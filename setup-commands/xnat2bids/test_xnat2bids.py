#!/usr/bin/env python
"""Tests for xnat2bids setup command: IntendedFor, TaskName, session directory."""

import json
import os
import shutil
import tempfile
import unittest


class TestBidsFieldmapModalities(unittest.TestCase):
    """Test that all expected fieldmap modalities are recognized."""

    def test_all_fieldmap_modalities_included(self):
        """All standard BIDS fieldmap modalities should be in the list."""
        # Import the module-level list
        # We can't easily import xnat2bids.py (it runs on import due to docopt),
        # so we test the expected values directly
        expected = ['phasemap', 'phasediff', 'magnitude1', 'magnitude2', 'fieldmap', 'epi']
        # Read the source and check
        src_path = os.path.join(os.path.dirname(__file__), 'xnat2bids.py')
        with open(src_path) as f:
            source = f.read()
        self.assertIn("'phasediff'", source)
        self.assertIn("'magnitude2'", source)
        self.assertIn("'fieldmap'", source)
        self.assertIn("'epi'", source)


class TestInjectIntendedFor(unittest.TestCase):
    """Test the injectIntendedFor function."""

    def setUp(self):
        """Create a temporary BIDS-like directory structure."""
        self.tmpdir = tempfile.mkdtemp()
        # Subject dir is parent of session dir
        self.subjectDir = os.path.join(self.tmpdir, 'sub-01')
        os.makedirs(self.subjectDir)

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _import_function(self):
        """Import injectIntendedFor without triggering docopt."""
        import types
        src_path = os.path.join(os.path.dirname(__file__), 'xnat2bids.py')
        with open(src_path) as f:
            source = f.read()

        # Extract just the function and its imports
        module = types.ModuleType('xnat2bids_test')
        module.__dict__['os'] = os
        module.__dict__['json'] = json
        import glob as glob_mod
        module.__dict__['glob'] = glob_mod.glob

        # Find and exec just the injectIntendedFor function
        lines = source.split('\n')
        func_lines = []
        in_func = False
        for line in lines:
            if line.startswith('def injectIntendedFor('):
                in_func = True
            elif in_func and line and not line[0].isspace() and not line.startswith('#'):
                break
            if in_func:
                func_lines.append(line)

        func_source = '\n'.join(func_lines)
        exec(func_source, module.__dict__)
        return module.__dict__['injectIntendedFor']

    def _create_session_with_fmap_and_func(self):
        """Create a session dir with fmap and func subdirectories."""
        sessionDir = os.path.join(self.subjectDir, 'ses-01')
        fmapDir = os.path.join(sessionDir, 'fmap')
        funcDir = os.path.join(sessionDir, 'func')
        os.makedirs(fmapDir)
        os.makedirs(funcDir)

        # Create fmap JSON sidecars
        for name in ['sub-01_ses-01_dir-AP_epi.json', 'sub-01_ses-01_dir-PA_epi.json']:
            with open(os.path.join(fmapDir, name), 'w') as f:
                json.dump({"PhaseEncodingDirection": "j"}, f)

        # Create func nifti files
        for name in ['sub-01_ses-01_task-rest_run-01_bold.nii.gz',
                      'sub-01_ses-01_task-rest_run-02_bold.nii.gz']:
            with open(os.path.join(funcDir, name), 'w') as f:
                f.write('')  # empty placeholder

        return sessionDir

    def test_injectIntendedFor_with_session(self):
        """IntendedFor should be injected with paths relative to subject dir."""
        injectIntendedFor = self._import_function()
        sessionDir = self._create_session_with_fmap_and_func()

        injectIntendedFor(sessionDir, self.subjectDir)

        # Check both fmap JSONs were patched
        fmapDir = os.path.join(sessionDir, 'fmap')
        for name in ['sub-01_ses-01_dir-AP_epi.json', 'sub-01_ses-01_dir-PA_epi.json']:
            with open(os.path.join(fmapDir, name)) as f:
                data = json.load(f)
            self.assertIn('IntendedFor', data)
            intended = data['IntendedFor']
            self.assertEqual(len(intended), 2)
            # Paths must be relative to subject dir
            self.assertEqual(intended[0], 'ses-01/func/sub-01_ses-01_task-rest_run-01_bold.nii.gz')
            self.assertEqual(intended[1], 'ses-01/func/sub-01_ses-01_task-rest_run-02_bold.nii.gz')

    def test_injectIntendedFor_preserves_existing_fields(self):
        """Existing JSON fields should be preserved when IntendedFor is added."""
        injectIntendedFor = self._import_function()
        sessionDir = self._create_session_with_fmap_and_func()

        injectIntendedFor(sessionDir, self.subjectDir)

        fmap_json = os.path.join(sessionDir, 'fmap', 'sub-01_ses-01_dir-AP_epi.json')
        with open(fmap_json) as f:
            data = json.load(f)
        # Original field should still be there
        self.assertEqual(data['PhaseEncodingDirection'], 'j')
        # IntendedFor should also be there
        self.assertIn('IntendedFor', data)

    def test_injectIntendedFor_no_fmap_dir(self):
        """Should silently return if no fmap directory exists."""
        injectIntendedFor = self._import_function()
        sessionDir = os.path.join(self.subjectDir, 'ses-01')
        funcDir = os.path.join(sessionDir, 'func')
        os.makedirs(funcDir)
        with open(os.path.join(funcDir, 'sub-01_bold.nii.gz'), 'w') as f:
            f.write('')

        # Should not raise
        injectIntendedFor(sessionDir, self.subjectDir)

    def test_injectIntendedFor_no_targets(self):
        """Should silently return if no func or dwi nifti files exist."""
        injectIntendedFor = self._import_function()
        sessionDir = os.path.join(self.subjectDir, 'ses-01')
        fmapDir = os.path.join(sessionDir, 'fmap')
        os.makedirs(fmapDir)
        with open(os.path.join(fmapDir, 'sub-01_epi.json'), 'w') as f:
            json.dump({}, f)

        injectIntendedFor(sessionDir, self.subjectDir)

        # JSON should NOT have IntendedFor since there are no targets
        with open(os.path.join(fmapDir, 'sub-01_epi.json')) as f:
            data = json.load(f)
        self.assertNotIn('IntendedFor', data)

    def test_injectIntendedFor_with_dwi(self):
        """IntendedFor should include dwi targets as well as func."""
        injectIntendedFor = self._import_function()
        sessionDir = os.path.join(self.subjectDir, 'ses-01')
        fmapDir = os.path.join(sessionDir, 'fmap')
        funcDir = os.path.join(sessionDir, 'func')
        dwiDir = os.path.join(sessionDir, 'dwi')
        os.makedirs(fmapDir)
        os.makedirs(funcDir)
        os.makedirs(dwiDir)

        with open(os.path.join(fmapDir, 'sub-01_ses-01_epi.json'), 'w') as f:
            json.dump({}, f)
        with open(os.path.join(funcDir, 'sub-01_ses-01_task-rest_bold.nii.gz'), 'w') as f:
            f.write('')
        with open(os.path.join(dwiDir, 'sub-01_ses-01_dwi.nii.gz'), 'w') as f:
            f.write('')

        injectIntendedFor(sessionDir, self.subjectDir)

        with open(os.path.join(fmapDir, 'sub-01_ses-01_epi.json')) as f:
            data = json.load(f)
        intended = data['IntendedFor']
        # func comes before dwi (alphabetical order of subdirs: dwi, func — but code iterates func first, then dwi)
        self.assertEqual(len(intended), 2)
        self.assertTrue(any('func/' in p for p in intended))
        self.assertTrue(any('dwi/' in p for p in intended))

    def test_injectIntendedFor_without_session(self):
        """IntendedFor should work when there are no sessions (destDirBase == subjectDir)."""
        injectIntendedFor = self._import_function()
        fmapDir = os.path.join(self.subjectDir, 'fmap')
        funcDir = os.path.join(self.subjectDir, 'func')
        os.makedirs(fmapDir)
        os.makedirs(funcDir)

        with open(os.path.join(fmapDir, 'sub-01_epi.json'), 'w') as f:
            json.dump({}, f)
        with open(os.path.join(funcDir, 'sub-01_task-rest_bold.nii.gz'), 'w') as f:
            f.write('')

        # When no sessions, destDirBase and subjectDir are the same
        injectIntendedFor(self.subjectDir, self.subjectDir)

        with open(os.path.join(fmapDir, 'sub-01_epi.json')) as f:
            data = json.load(f)
        intended = data['IntendedFor']
        self.assertEqual(len(intended), 1)
        # Path should be relative to subject dir (no ses- prefix)
        self.assertEqual(intended[0], 'func/sub-01_task-rest_bold.nii.gz')

    def test_injectIntendedFor_uses_forward_slashes(self):
        """IntendedFor paths must use forward slashes per BIDS spec."""
        injectIntendedFor = self._import_function()
        sessionDir = self._create_session_with_fmap_and_func()

        injectIntendedFor(sessionDir, self.subjectDir)

        fmap_json = os.path.join(sessionDir, 'fmap', 'sub-01_ses-01_dir-AP_epi.json')
        with open(fmap_json) as f:
            data = json.load(f)
        for path in data['IntendedFor']:
            self.assertNotIn('\\', path, "IntendedFor paths must use forward slashes")
            self.assertIn('/', path)

    def test_injectIntendedFor_only_nii_gz(self):
        """IntendedFor should only include .nii.gz files, not .json sidecars."""
        injectIntendedFor = self._import_function()
        sessionDir = os.path.join(self.subjectDir, 'ses-01')
        fmapDir = os.path.join(sessionDir, 'fmap')
        funcDir = os.path.join(sessionDir, 'func')
        os.makedirs(fmapDir)
        os.makedirs(funcDir)

        with open(os.path.join(fmapDir, 'sub-01_epi.json'), 'w') as f:
            json.dump({}, f)
        # Create both .nii.gz and .json in func
        with open(os.path.join(funcDir, 'sub-01_task-rest_bold.nii.gz'), 'w') as f:
            f.write('')
        with open(os.path.join(funcDir, 'sub-01_task-rest_bold.json'), 'w') as f:
            json.dump({}, f)

        injectIntendedFor(sessionDir, self.subjectDir)

        with open(os.path.join(fmapDir, 'sub-01_epi.json')) as f:
            data = json.load(f)
        intended = data['IntendedFor']
        self.assertEqual(len(intended), 1)
        self.assertTrue(intended[0].endswith('.nii.gz'))


class TestInjectTaskName(unittest.TestCase):
    """Test the injectTaskName function."""

    def setUp(self):
        self.tmpdir = tempfile.mkdtemp()

    def tearDown(self):
        shutil.rmtree(self.tmpdir)

    def _import_function(self):
        """Import injectTaskName without triggering docopt."""
        import types
        src_path = os.path.join(os.path.dirname(__file__), 'xnat2bids.py')
        with open(src_path) as f:
            source = f.read()

        module = types.ModuleType('xnat2bids_test')
        module.__dict__['os'] = os
        module.__dict__['json'] = json
        import glob as glob_mod
        module.__dict__['glob'] = glob_mod.glob

        # Extract generateBidsNameMap (dependency) and injectTaskName
        lines = source.split('\n')
        for func_name in ['generateBidsNameMap', 'injectTaskName']:
            func_lines = []
            in_func = False
            for line in lines:
                if line.startswith('def {}('.format(func_name)):
                    in_func = True
                elif in_func and line and not line[0].isspace() and not line.startswith('#'):
                    break
                if in_func:
                    func_lines.append(line)
            exec('\n'.join(func_lines), module.__dict__)

        return module.__dict__['injectTaskName']

    def test_injects_taskname_from_filename(self):
        """TaskName should be derived from task-<label> in the filename."""
        injectTaskName = self._import_function()
        funcDir = os.path.join(self.tmpdir, 'func')
        os.makedirs(funcDir)

        sidecar = os.path.join(funcDir, 'sub-01_ses-01_task-rest_bold.json')
        with open(sidecar, 'w') as f:
            json.dump({"RepetitionTime": 2.0}, f)

        injectTaskName(self.tmpdir)

        with open(sidecar) as f:
            data = json.load(f)
        self.assertEqual(data['TaskName'], 'rest')
        self.assertEqual(data['RepetitionTime'], 2.0)

    def test_skips_when_taskname_exists(self):
        """Should not overwrite existing TaskName."""
        injectTaskName = self._import_function()
        funcDir = os.path.join(self.tmpdir, 'func')
        os.makedirs(funcDir)

        sidecar = os.path.join(funcDir, 'sub-01_task-rest_bold.json')
        with open(sidecar, 'w') as f:
            json.dump({"TaskName": "My Custom Name"}, f)

        injectTaskName(self.tmpdir)

        with open(sidecar) as f:
            data = json.load(f)
        self.assertEqual(data['TaskName'], 'My Custom Name')

    def test_skips_non_task_files(self):
        """Files without task- entity should be left alone."""
        injectTaskName = self._import_function()
        funcDir = os.path.join(self.tmpdir, 'func')
        os.makedirs(funcDir)

        sidecar = os.path.join(funcDir, 'sub-01_bold.json')
        with open(sidecar, 'w') as f:
            json.dump({"RepetitionTime": 2.0}, f)

        injectTaskName(self.tmpdir)

        with open(sidecar) as f:
            data = json.load(f)
        self.assertNotIn('TaskName', data)

    def test_no_func_dir(self):
        """Should silently return if no func directory exists."""
        injectTaskName = self._import_function()
        # tmpdir has no func/ subdir
        injectTaskName(self.tmpdir)  # Should not raise

    def test_multiple_tasks(self):
        """Each sidecar should get the correct task label from its filename."""
        injectTaskName = self._import_function()
        funcDir = os.path.join(self.tmpdir, 'func')
        os.makedirs(funcDir)

        for task in ['rest', 'nback', 'motor']:
            sidecar = os.path.join(funcDir, 'sub-01_task-{}_bold.json'.format(task))
            with open(sidecar, 'w') as f:
                json.dump({}, f)

        injectTaskName(self.tmpdir)

        for task in ['rest', 'nback', 'motor']:
            sidecar = os.path.join(funcDir, 'sub-01_task-{}_bold.json'.format(task))
            with open(sidecar) as f:
                data = json.load(f)
            self.assertEqual(data['TaskName'], task)


class TestSessionDirectoryDetection(unittest.TestCase):
    """Test that generateBidsNameMap correctly parses ses- entity from filenames.

    The session directory fix relies on generateBidsNameMap returning 'ses' in
    the name map when filenames contain a ses- entity. This test verifies that
    parsing works correctly so the main script can detect when to create a
    session subdirectory.
    """

    def _import_function(self):
        """Import generateBidsNameMap without triggering docopt."""
        import types
        src_path = os.path.join(os.path.dirname(__file__), 'xnat2bids.py')
        with open(src_path) as f:
            source = f.read()

        module = types.ModuleType('xnat2bids_test')
        module.__dict__['os'] = os

        lines = source.split('\n')
        func_lines = []
        in_func = False
        for line in lines:
            if line.startswith('def generateBidsNameMap('):
                in_func = True
            elif in_func and line and not line[0].isspace() and not line.startswith('#'):
                break
            if in_func:
                func_lines.append(line)

        exec('\n'.join(func_lines), module.__dict__)
        return module.__dict__['generateBidsNameMap']

    def test_parses_session_entity(self):
        """Filenames with ses- should have 'ses' in the name map."""
        generateBidsNameMap = self._import_function()
        nameMap = generateBidsNameMap('sub-XYZ01_ses-XYZ01d2_T1w')
        self.assertEqual(nameMap.get('ses'), 'XYZ01d2')

    def test_no_session_entity(self):
        """Filenames without ses- should not have 'ses' in the name map."""
        generateBidsNameMap = self._import_function()
        nameMap = generateBidsNameMap('sub-XYZ01_T1w')
        self.assertIsNone(nameMap.get('ses'))

    def test_parses_task_entity(self):
        """Filenames with task- should have 'task' in the name map."""
        generateBidsNameMap = self._import_function()
        nameMap = generateBidsNameMap('sub-01_ses-01_task-rest_run-01_bold')
        self.assertEqual(nameMap.get('task'), 'rest')
        self.assertEqual(nameMap.get('ses'), '01')
        self.assertEqual(nameMap.get('run'), '01')

    def test_complex_session_label(self):
        """Long session labels (like XNAT timestamps) should parse correctly."""
        generateBidsNameMap = self._import_function()
        nameMap = generateBidsNameMap('sub-XYZ01_ses-20250101120000_task-memory_run-03_bold')
        self.assertEqual(nameMap.get('ses'), '20250101120000')
        self.assertEqual(nameMap.get('task'), 'memory')
        self.assertEqual(nameMap.get('run'), '03')


if __name__ == '__main__':
    unittest.main()
