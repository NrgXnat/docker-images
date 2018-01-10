# Slicer Command Notes

Part of the information on running slicer executables in a docker image comes from a google doc by John Flavin and Andrey Federov: [Notes on Schemas for Command Line Executables / Docker Images](https://docs.google.com/document/d/1XRLWm_gJj8YC7TagihQd8DQfqT1XSTm1SMOCzfxEfqM/edit).

Per those notes, there are two docker images that can be used for slicer:
## Official image
[Docker Hub](https://hub.docker.com/r/slicer/slicer-build/)

According to Andrey Federov, "Takes very long time to run commands from there."

Example

    docker run -ti slicer/slicer-build /usr/src/Slicer-build/Slicer-build/Slicer --launch RobustStatisticsSegmenter --help

## Unofficial image
[Quay.io](https://quay.io/repository/fedorov/slicerdockers)

Maintained by Andrey Federov, who says this "simply pulls and unpacks the binary build".

Example

    docker run -ti quay.io/fedorov/slicerdockers:4.8.1 /opt/slicer/Slicer --launch RobustStatisticsSegmenter --help

## Executables
Inside `quay.io/federov/slicerdockers:4.8.1` at path `/opt/slicer/lib/Slicer-4.8/cli-modules`.

* ACPCTransform
* AddScalarVolumes
* BRAINSDWICleanup
* BRAINSDemonWarp
* BRAINSFit
* BRAINSLabelStats
* BRAINSROIAuto
* BRAINSResample
* BRAINSResize
* BRAINSStripRotation
* BRAINSTransformConvert
* CastScalarVolume
* CheckerBoardFilter
* CreateDICOMSeries
* CurvatureAnisotropicDiffusion
* DWIConvert
* EMSegmentCommandLine
* EMSegmentTransformToNewFormat
* ExecutionModelTour
* ExpertAutomatedRegistration
* ExtractSkeleton
* FiducialRegistration
* GaussianBlurImageFilter
* GradientAnisotropicDiffusion
* GrayscaleFillHoleImageFilter
* GrayscaleGrindPeakImageFilter
* GrayscaleModelMaker
* HistogramMatching
* ImageLabelCombine
* IslandRemoval
* LabelMapSmoothing
* MaskScalarVolume
* MedianImageFilter
* MergeModels
* ModelMaker
* ModelToLabelMap
* MultiplyScalarVolumes
* N4ITKBiasFieldCorrection
* OrientScalarVolume
* OtsuThresholdImageFilter
* PETStandardUptakeValueComputation
* PerformMetricTest
* ProbeVolumeWithModel
* ResampleDTIVolume
* ResampleScalarVectorDWIVolume
* ResampleScalarVolume
* RobustStatisticsSegmenter
* SimpleRegionGrowingSegmentation
* SubtractScalarVolumes
* ThresholdScalarVolume
* VBRAINSDemonWarp
* VotingBinaryHoleFillingImageFilter

ACPCTransform AddScalarVolumes BRAINSDWICleanup BRAINSDemonWarp BRAINSFit BRAINSLabelStats BRAINSROIAuto BRAINSResample BRAINSResize BRAINSStripRotation BRAINSTransformConvert CastScalarVolume CheckerBoardFilter CreateDICOMSeries CurvatureAnisotropicDiffusion DWIConvert EMSegmentCommandLine EMSegmentTransformToNewFormat ExecutionModelTour ExpertAutomatedRegistration ExtractSkeleton FiducialRegistration GaussianBlurImageFilter GradientAnisotropicDiffusion GrayscaleFillHoleImageFilter GrayscaleGrindPeakImageFilter GrayscaleModelMaker HistogramMatching ImageLabelCombine IslandRemoval LabelMapSmoothing MaskScalarVolume MedianImageFilter MergeModels ModelMaker ModelToLabelMap MultiplyScalarVolumes N4ITKBiasFieldCorrection OrientScalarVolume OtsuThresholdImageFilter PETStandardUptakeValueComputation PerformMetricTest ProbeVolumeWithModel ResampleDTIVolume ResampleScalarVectorDWIVolume ResampleScalarVolume RobustStatisticsSegmenter SimpleRegionGrowingSegmentation SubtractScalarVolumes ThresholdScalarVolume VBRAINSDemonWarp VotingBinaryHoleFillingImageFilter

### ACPCTransform

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ACPCTransform
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-d]
                                            [--outputTransform <std::string>]
                                            [--midline
                                            <std::vector<std::vector<float> >>]
                                            ...  [--acpc
                                            <std::vector<std::vector<float> >>]
                                            ...  [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -d,  --
         Click this checkbox to see debugging output. (value: 0)

       --outputTransform <std::string>
         A transform filled in from the ACPC and Midline registration
         calculation.

       --midline <std::vector<std::vector<float> >>  (accepted multiple times)
         The midline is a series of points defining the division between the
         hemispheres of the brain (the mid sagittal plane). (value: None)

       --acpc <std::vector<std::vector<float> >>  (accepted multiple times)
         ACPC line, a list of two fiducial points, one at the anterior
         commissure and one at the posterior commissure. (value: None)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: <p>Calculate a transformation from two lists of fiducial
       points.</p><p>The ACPC line extends between two points, one at the
       anterior commissure and one at the posterior commissure. The resulting
       transform will bring the line connecting the two points horizontal to
       the AP axis.</p><p>The midline is a series of points defining the
       division between the hemispheres of the brain (the mid sagittal plane).
       The resulting transform will result in the output volume having the mid
       sagittal plane lined up with the AS plane.</p><p>Use the Filtering
       module <b>Resample Scalar/Vector/DWI Volume</b> to apply the
       transformation to a volume.</p>

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL,
       BWH)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### AddScalarVolumes

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./AddScalarVolumes
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--order <0|1|2|3>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --order <0|1|2|3>
         Interpolation order if two images are in different coordinate frames
         or have different sampling. (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume 1

       <std::string>
         (required)  Input volume 2

       <std::string>
         (required)  Volume1 + Volume2


       Description: Adds two images. Although all image types are supported on
       input, only signed types are produced. The two images do not have to
       have the same dimensions.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### BRAINSDWICleanup

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSDWICleanup
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-b
                                            <std::vector<int>>] [-o
                                            <std::string>] [-i <std::string>]
                                            [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -b <std::vector<int>>,  --badGradients <std::vector<int>>

       -o <std::string>,  --outputVolume <std::string>
         given a list of

       -i <std::string>,  --inputVolume <std::string>
         Required: input image is a 4D NRRD image.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Remove bad gradients/volumes from DWI NRRD file.

       Author(s): This tool was developed by Kent Williams.


### BRAINSDemonWarp

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSDemonWarp
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfThreads <int>]
                                            [--numberOfBCHApproximationTerms
                                            <int>] [-p] [-G] [-a] [-l <double>]
                                            [-g <double>] [-t <0|1|2>] [-v]
                                            [--outputNormalized]
                                            [--checkerboardPatternSubdivisions
                                            <std::vector<int>>]
                                            [--outputCheckerboardVolume
                                            <std::string>]
                                            [--outputDisplacementFieldPrefix
                                            <std::string>]
                                            [--neighborhoodForBOBF
                                            <std::vector<int>>] [--seedForBOBF
                                            <std::vector<int>>]
                                            [--backgroundFillValue <int>]
                                            [--upperThresholdForBOBF <int>]
                                            [--lowerThresholdForBOBF <int>]
                                            [--movingBinaryVolume
                                            <std::string>] [--fixedBinaryVolume
                                            <std::string>]
                                            [--maskProcessingMode <NOMASK
                                            |ROIAUTO|ROI|BOBF>]
                                            [--initializeWithTransform
                                            <std::string>]
                                            [--initializeWithDisplacementField
                                            <std::string>] [--medianFilterSize
                                            <std::vector<int>>]
                                            [--numberOfMatchPoints <int>]
                                            [--numberOfHistogramBins <int>]
                                            [-e] [-i <std::vector<int>>]
                                            [--minimumMovingPyramid
                                            <std::vector<int>>]
                                            [--minimumFixedPyramid
                                            <std::vector<int>>] [-n <int>] [-s
                                            <double>] [--registrationFilterType
                                            <Demons|FastSymmetricForces
                                            |Diffeomorphic>]
                                            [--interpolationMode
                                            <NearestNeighbor|Linear
                                            |ResampleInPlace|BSpline
                                            |WindowedSinc|Hamming|Cosine|Welch
                                            |Lanczos|Blackman>]
                                            [--outputPixelType <float|short
                                            |ushort|int|uchar>] [-O
                                            <std::string>] [-o <std::string>]
                                            [--inputPixelType <float|short
                                            |ushort|int|uchar>] [-f
                                            <std::string>] [-m <std::string>]
                                            [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfThreads <int>
         Explicitly specify the maximum number of threads to use. (value: -1)

       --numberOfBCHApproximationTerms <int>
         Number of terms in the BCH expansion (value: 2)

       -p,  --promptUser
         Prompt the user to hit enter each time an image is sent to the
         DebugImageViewer (value: 0)

       -G,  --gui
         Display intermediate image volumes for debugging (value: 0)

       -a,  --use_vanilla_dem
         Run vanilla demons algorithm (value: 0)

       -l <double>,  --max_step_length <double>
         Maximum length of an update vector (0: no restriction) (value: 2)

       -g <double>,  --upFieldSmoothing <double>
         Smoothing sigma for the update field at each iteration (value: 0)

       -t <0|1|2>,  --gradient_type <0|1|2>
         Type of gradient used for computing the demons force (0 is symmetrized
         , 1 is fixed image, 2 is moving image) (value: 0)

       -v,  --outputDebug
         Flag to write debugging images after each step. (value: 0)

       --outputNormalized
         Flag to warp and write the normalized images to output.  In normalized
         images the image values are fit-scaled to be between 0 and the maximum
         storage type value. (value: 0)

       --checkerboardPatternSubdivisions <std::vector<int>>
         Number of Checkerboard subdivisions in all 3 directions (value: 4,4,4)

       --outputCheckerboardVolume <std::string>
         Genete a checkerboard image volume between the fixedVolume and the
         deformed movingVolume.

       --outputDisplacementFieldPrefix <std::string>
         Displacement field filename prefix for writing separate x, y, and z
         component images (value: none)

       --neighborhoodForBOBF <std::vector<int>>
         neighborhood in all 3 directions to be included when performing BOBF
         (value: 1,1,1)

       --seedForBOBF <std::vector<int>>
         coordinates in all 3 directions for Seed when performing BOBF (value:
         0,0,0)

       --backgroundFillValue <int>
         Replacement value to overwrite background when performing BOBF (value:
         0)

       --upperThresholdForBOBF <int>
         Upper threshold for performing BOBF (value: 70)

       --lowerThresholdForBOBF <int>
         Lower threshold for performing BOBF (value: 0)

       --movingBinaryVolume <std::string>
         Mask filename for desired region of interest in the Moving image.

       --fixedBinaryVolume <std::string>
         Mask filename for desired region of interest in the Fixed image.

       --maskProcessingMode <NOMASK|ROIAUTO|ROI|BOBF>
         What mode to use for using the masks: NOMASK|ROIAUTO|ROI|BOBF.  If
         ROIAUTO is choosen, then the mask is implicitly defined using a otsu
         forground and hole filling algorithm. Where the Region Of Interest
         mode uses the masks to define what parts of the image should be used
         for computing the deformation field.  Brain Only Background Fill uses
         the masks to pre-process the input images by clipping and filling in
         the background with a predefined value. (value: NOMASK)

       --initializeWithTransform <std::string>
         Initial Transform filename

       --initializeWithDisplacementField <std::string>
         Initial deformation field vector image file name

       --medianFilterSize <std::vector<int>>
         Median filter radius in all 3 directions.  When images have a lot of
         salt and pepper noise, this step can improve the registration. (value:
         0,0,0)

       --numberOfMatchPoints <int>
         The number of match points for histrogramMatch (value: 2)

       --numberOfHistogramBins <int>
         The number of histogram levels (value: 256)

       -e,  --histogramMatch
         Histogram Match the input images.  This is suitable for images of the
         same modality that may have different absolute scales, but the same
         overall intensity profile. (value: 0)

       -i <std::vector<int>>,  --arrayOfPyramidLevelIterations
          <std::vector<int>>
         The number of iterations for each pyramid level (value: 300,50,30,20
         ,15)

       --minimumMovingPyramid <std::vector<int>>
         The shrink factor for the first level of the moving image pyramid.
         (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally
         full scale) (value: 16,16,16)

       --minimumFixedPyramid <std::vector<int>>
         The shrink factor for the first level of the fixed image pyramid.
         (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally
         full scale) (value: 16,16,16)

       -n <int>,  --numberOfPyramidLevels <int>
         Number of image pyramid levels to use in the multi-resolution
         registration. (value: 5)

       -s <double>,  --smoothDisplacementFieldSigma <double>
         A gaussian smoothing value to be applied to the deformation feild at
         each iteration. (value: 1)

       --registrationFilterType <Demons|FastSymmetricForces|Diffeomorphic>
         Registration Filter Type: Demons|FastSymmetricForces|Diffeomorphic
         (value: Diffeomorphic)

       --interpolationMode <NearestNeighbor|Linear|ResampleInPlace|BSpline
          |WindowedSinc|Hamming|Cosine|Welch|Lanczos|Blackman>
         Type of interpolation to be used when applying transform to moving
         volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline
         , or WindowedSinc (value: Linear)

       --outputPixelType <float|short|ushort|int|uchar>
         outputVolume will be typecast to this format: float|short|ushort|int
         |uchar (value: float)

       -O <std::string>,  --outputDisplacementFieldVolume <std::string>
         Output deformation field vector image (will have the same physical
         space as the fixedVolume).

       -o <std::string>,  --outputVolume <std::string>
         Required: output resampled moving image (will have the same physical
         space as the fixedVolume).

       --inputPixelType <float|short|ushort|int|uchar>
         Input volumes will be typecast to this format: float|short|ushort|int
         |uchar (value: float)

       -f <std::string>,  --fixedVolume <std::string>
         Required: input fixed (target) image

       -m <std::string>,  --movingVolume <std::string>
         Required: input moving image

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This program finds a deformation field to warp a moving
       image onto a fixed image.  The images must be of the same signal kind,
       and contain an image of the same kind of object.  This program uses the
       Thirion Demons warp software in ITK, the Insight Toolkit.  Additional
       information is available at:
       http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/BR
       AINSDemonWarp.

       Author(s): This tool was developed by Hans J. Johnson and Greg
       Harris.

       Acknowledgements: The development of this tool was supported by funding
       from grants NS050568 and NS40068 from the National Institute of
       Neurological Disorders and Stroke and grants MH31593, MH40856, from the
       National Institute of Mental Health.


### BRAINSFit

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSFit
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-v]
                                            [--logFileReport <std::string>]
                                            [--metricSamplingStrategy <Random>]
                                            [-p] [-G]
                                            [--maximumNumberOfCorrections
                                            <int>]
                                            [--maximumNumberOfEvaluations
                                            <int>]
                                            [--projectedGradientTolerance
                                            <double>]
                                            [--costFunctionConvergenceFactor
                                            <double>] [--debugLevel <int>]
                                            [--numberOfThreads <int>]
                                            [--writeTransformOnFailure]
                                            [--failureExitCode <int>]
                                            [--writeOutputTransformInFloat]
                                            [--initializeRegistrationByCurrentG
                                            enericTransform] [--outputTransform
                                            <std::string>] [--transformType
                                            <std::vector<std::string>>]
                                            [--strippedOutputTransform
                                            <std::string>] [--numberOfSamples
                                            <int>] [--ROIAutoClosingSize
                                            <double>] [--ROIAutoDilateSize
                                            <double>]
                                            [--maskInferiorCutOffFromCenter
                                            <double>] [--costMetric <MMI|MSE|NC
                                            |MIH>] [--numberOfMatchPoints
                                            <int>] [--numberOfHistogramBins
                                            <int>] [--movingVolumeTimeIndex
                                            <int>] [--fixedVolumeTimeIndex
                                            <int>] [--maxBSplineDisplacement
                                            <double>] [--skewScale <double>]
                                            [--reproportionScale <double>]
                                            [--translationScale <double>]
                                            [--relaxationFactor <double>]
                                            [--minimumStepLength
                                            <std::vector<double>>]
                                            [--maximumStepLength <double>]
                                            [--numberOfIterations
                                            <std::vector<int>>]
                                            [--interpolationMode
                                            <NearestNeighbor|Linear
                                            |ResampleInPlace|BSpline
                                            |WindowedSinc|Hamming|Cosine|Welch
                                            |Lanczos|Blackman>]
                                            [--scaleOutputValues]
                                            [--backgroundFillValue <double>]
                                            [--outputVolumePixelType <float
                                            |short|ushort|int|uint|uchar>]
                                            [--movingVolume2 <std::string>]
                                            [--fixedVolume2 <std::string>]
                                            [--removeIntensityOutliers
                                            <double>] [--medianFilterSize
                                            <std::vector<int>>] [-e]
                                            [--useROIBSpline]
                                            [--outputMovingVolumeROI
                                            <std::string>]
                                            [--outputFixedVolumeROI
                                            <std::string>]
                                            [--movingBinaryVolume
                                            <std::string>] [--fixedBinaryVolume
                                            <std::string>]
                                            [--maskProcessingMode <NOMASK
                                            |ROIAUTO|ROI>] [--useComposite]
                                            [--useSyN] [--useBSpline]
                                            [--useAffine]
                                            [--useScaleSkewVersor3D]
                                            [--useScaleVersor3D] [--useRigid]
                                            [--initializeTransformMode <Off
                                            |useMomentsAlign
                                            |useCenterOfHeadAlign
                                            |useGeometryAlign
                                            |useCenterOfROIAlign>]
                                            [--initialTransform <std::string>]
                                            [--outputVolume <std::string>]
                                            [--bsplineTransform <std::string>]
                                            [--linearTransform <std::string>]
                                            [--splineGridSize
                                            <std::vector<int>>]
                                            [--samplingPercentage <double>]
                                            [--movingVolume <std::string>]
                                            [--fixedVolume <std::string>] [--]
                                            [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -v,  --
          (value: 0)

       --logFileReport <std::string>
         A file to write out final information report in CSV file: MetricName
         ,MetricValue,FixedImageName,FixedMaskName,MovingImageName
         ,MovingMaskName

       --metricSamplingStrategy <Random>
         It defines the method that registration filter uses to sample the
         input fixed image. Only Random is supported for now. (value: Random)

       -p,  --promptUser
         Prompt the user to hit enter each time an image is sent to the
         DebugImageViewer (value: 0)

       -G,  --gui
         Display intermediate image volumes for debugging.  NOTE:  This is not
         part of the standard build sytem, and probably does nothing on your
         installation. (value: 0)

       --maximumNumberOfCorrections <int>
         Maximum number of corrections in lbfgsb optimizer. (value: 25)

       --maximumNumberOfEvaluations <int>
         Maximum number of evaluations for line search in lbfgsb optimizer.
         (value: 900)

       --projectedGradientTolerance <double>
         From itkLBFGSBOptimizer.h: Set/Get the ProjectedGradientTolerance.
         Algorithm terminates when the project gradient is below the tolerance.
         Default lbfgsb value is 1e-5, but 1e-4 seems to work well. (value:
         1e-05)

       --costFunctionConvergenceFactor <double>
         From itkLBFGSBOptimizer.h: Set/Get the CostFunctionConvergenceFactor.
         Algorithm terminates when the reduction in cost function is less than
         (factor * epsmcj) where epsmch is the machine precision. Typical
         values for factor: 1e+12 for low accuracy; 1e+7 for moderate accuracy
         and 1e+1 for extremely high accuracy.  1e+9 seems to work well.
         (value: 2e+13)

       --debugLevel <int>
         Display debug messages, and produce debug intermediate results.  0=OFF
         , 1=Minimal, 10=Maximum debugging. (value: 0)

       --numberOfThreads <int>
         Explicitly specify the maximum number of threads to use. (default is
         auto-detected) (value: -1)

       --writeTransformOnFailure
         Flag to save the final transform even if the numberOfIterations are
         reached without convergence. (Intended for use when --failureExitCode
         0 ) (value: 0)

       --failureExitCode <int>
         If the fit fails, exit with this status code.  (It can be used to
         force a successfult exit status of (0) if the registration fails due
         to reaching the maximum number of iterations. (value: -1)

       --writeOutputTransformInFloat
         By default, the output registration transforms (either the output
         composite transform or each transform component) are written to the
         disk in double precision. If this flag is ON, the output transforms
         will be written in single (float) precision. It is especially
         important if the output transform is a displacement field transform,
         or it is a composite transform that includes several displacement
         fields. (value: 0)

       --initializeRegistrationByCurrentGenericTransform
         If this flag is ON, the current generic composite transform, resulted
         from the linear registration stages, is set to initialize the follow
         nonlinear registration process. However, by the default behaviour, the
         moving image is first warped based on the existant transform before it
         is passed to the BSpline registration filter. It is done to speed up
         the BSpline registration by reducing the computations of composite
         transform Jacobian. (value: 0)

       --outputTransform <std::string>
         (optional) Filename to which save the (optional) estimated transform.
         NOTE: You must select either the outputTransform or the outputVolume
         option.

       --transformType <std::vector<std::string>>
         Specifies a list of registration types to be used.  The valid types
         are, Rigid, ScaleVersor3D, ScaleSkewVersor3D, Affine, BSpline and SyN.
         Specifying more than one in a comma separated list will initialize the
         next stage with the previous results. If registrationClass flag is
         used, it overrides this parameter setting.

       --strippedOutputTransform <std::string>
         Rigid component of the estimated affine transform. Can be used to
         rigidly register the moving image to the fixed image. NOTE:  This
         value is overridden if either bsplineTransform or linearTransform is
         set.

       --numberOfSamples <int>
         The number of voxels sampled for mutual information computation.
         Increase this for higher accuracy, at the cost of longer computation
         time.

         NOTE that it is suggested to use samplingPercentage instead of this
         option. However, if set to non-zero, numberOfSamples overwrites the
         samplingPercentage option. (value: 0)

       --ROIAutoClosingSize <double>
         This flag is only relevant when using ROIAUTO mode for initializing
         masks.  It defines the hole closing size in mm.  It is rounded up to
         the nearest whole pixel size in each direction. The default is to use
         a closing size of 9mm.  For mouse data this value may need to be reset
         to 0.9 or smaller. (value: 9)

       --ROIAutoDilateSize <double>
         This flag is only relevant when using ROIAUTO mode for initializing
         masks.  It defines the final dilation size to capture a bit of
         background outside the tissue region.  A setting of 10mm has been
         shown to help regularize a BSpline registration type so that there is
         some background constraints to match the edges of the head better.
         (value: 0)

       --maskInferiorCutOffFromCenter <double>
         If Initialize Transform Mode is set to useCenterOfHeadAlign or Masking
         Option is ROIAUTO then this value defines the how much is cut of from
         the inferior part of the image. The cut-off distance is specified in
         millimeters, relative to the image center. If the value is 1000 or
         larger then no cut-off performed. (value: 1000)

       --costMetric <MMI|MSE|NC|MIH>
         The cost metric to be used during fitting. Defaults to MMI. Options
         are MMI (Mattes Mutual Information), MSE (Mean Square Error), NC
         (Normalized Correlation), MC (Match Cardinality for binary images)
         (value: MMI)

       --numberOfMatchPoints <int>
         Number of histogram match points used for mutual information metric
         estimation. (value: 10)

       --numberOfHistogramBins <int>
         The number of histogram levels used for mutual information metric
         estimation. (value: 50)

       --movingVolumeTimeIndex <int>
         The index in the time series for the 3D moving image to fit. Only
         allowed if the moving input volume is 4-dimensional (value: 0)

       --fixedVolumeTimeIndex <int>
         The index in the time series for the 3D fixed image to fit. Only
         allowed if the fixed input volume is 4-dimensional. (value: 0)

       --maxBSplineDisplacement <double>
         Maximum allowed displacements in image physical coordinates (mm) for
         BSpline control grid along each axis.  A value of 0.0 indicates that
         the problem should be unbounded.  NOTE:  This only constrains the
         BSpline portion, and does not limit the displacement from the
         associated bulk transform.  This can lead to a substantial reduction
         in computation time in the BSpline optimizer. (value: 0)

       --skewScale <double>
         ScaleSkewVersor3D Skew compensation factor.  Increase this to allow
         for more skew in a ScaleSkewVersor3D search pattern.  1.0 works well
         with a translationScale of 1000.0 (value: 1)

       --reproportionScale <double>
         ScaleVersor3D 'Scale' compensation factor.  Increase this to allow for
         more rescaling in a ScaleVersor3D or ScaleSkewVersor3D search pattern.
         1.0 works well with a translationScale of 1000.0 (value: 1)

       --translationScale <double>
         How much to scale up changes in position (in mm) compared to unit
         rotational changes (in radians) -- decrease this to allow for more
         rotation in the search pattern. (value: 1000)

       --relaxationFactor <double>
         Specifies how quickly the optimization step length is decreased during
         registration. The value must be larger than 0 and smaller than 1.
         Larger values result in slower step size decrease, which allow for
         recovering larger initial misalignments but it increases the
         registration time and the chance that the registration will not
         converge. (value: 0.5)

       --minimumStepLength <std::vector<double>>
         Each step in the optimization takes steps at least this big.  When
         none are possible, registration is complete. Smaller values allows the
         optimizer to make smaller adjustments, but the registration time may
         increase. (value: 0.001)

       --maximumStepLength <double>
         Starting step length of the optimizer. In general, higher values allow
         for recovering larger initial misalignments but there is an increased
         chance that the registration will not converge. (value: 0.05)

       --numberOfIterations <std::vector<int>>
         The maximum number of iterations to try before stopping the
         optimization. When using a lower value (500-1000) then the
         registration is forced to terminate earlier but there is a higher risk
         of stopping before an optimal solution is reached. (value: 1500)

       --interpolationMode <NearestNeighbor|Linear|ResampleInPlace|BSpline
          |WindowedSinc|Hamming|Cosine|Welch|Lanczos|Blackman>
         Type of interpolation to be used when applying transform to moving
         volume.  Options are Linear, NearestNeighbor, BSpline, WindowedSinc,
         Hamming, Cosine, Welch, Lanczos, or ResampleInPlace.  The
         ResampleInPlace option will create an image with the same discrete
         voxel values and will adjust the origin and direction of the physical
         space interpretation. (value: Linear)

       --scaleOutputValues
         If true, and the voxel values do not fit within the minimum and
         maximum values of the desired outputVolumePixelType, then linearly
         scale the min/max output image voxel values to fit within the min/max
         range of the outputVolumePixelType. (value: 0)

       --backgroundFillValue <double>
         This value will be used for filling those areas of the output image
         that have no corresponding voxels in the input moving image. (value:
         0)

       --outputVolumePixelType <float|short|ushort|int|uint|uchar>
         Data type for representing a voxel of the Output Volume. (value:
         float)

       --movingVolume2 <std::string>
         Input moving image that will be used for multimodal registration(this
         image will be transformed into the fixed image space).

       --fixedVolume2 <std::string>
         Input fixed image that will be used for multimodal registration. (the
         moving image will be transformed into this image space).

       --removeIntensityOutliers <double>
         Remove very high and very low intensity voxels from the input volumes.
         The parameter specifies the half percentage to decide outliers of
         image intensities. The default value is zero, which means no outlier
         removal. If the value of 0.005 is given, the 0.005% of both tails will
         be thrown away, so 0.01% of intensities in total would be ignored in
         the statistic calculation. (value: 0)

       --medianFilterSize <std::vector<int>>
         Apply median filtering to reduce noise in the input volumes. The 3
         values specify the radius for the optional MedianImageFilter
         preprocessing in all 3 directions (in voxels). (value: 0,0,0)

       -e,  --histogramMatch
         Apply histogram matching operation for the input images to make them
         more similar.  This is suitable for images of the same modality that
         may have different brightness or contrast, but the same overall
         intensity profile. Do NOT use if registering images from different
         modalities. (value: 0)

       --useROIBSpline
         If enabled then the bounding box of the input ROIs defines the BSpline
         grid support region. Otherwise the BSpline grid support region is the
         whole fixed image. (value: 0)

       --outputMovingVolumeROI <std::string>
         ROI that is automatically computed from the moving image. Only
         available if Masking Option is ROIAUTO. Image areas where the mask
         volume has zero value are ignored during the registration.

       --outputFixedVolumeROI <std::string>
         ROI that is automatically computed from the fixed image. Only
         available if Masking Option is ROIAUTO. Image areas where the mask
         volume has zero value are ignored during the registration.

       --movingBinaryVolume <std::string>
         Moving Image binary mask volume, required if Masking Option is ROI.
         Image areas where the mask volume has zero value are ignored during
         the registration.

       --fixedBinaryVolume <std::string>
         Fixed Image binary mask volume, required if Masking Option is ROI.
         Image areas where the mask volume has zero value are ignored during
         the registration.

       --maskProcessingMode <NOMASK|ROIAUTO|ROI>
         Specifies a mask to only consider a certain image region for the
         registration.  If ROIAUTO is chosen, then the mask is computed using
         Otsu thresholding and hole filling. If ROI is chosen then the mask has
         to be specified as in input. (value: NOMASK)

       --useComposite
         Perform a Composite registration as part of the sequential
         registration steps.  This family of options overrides the use of
         transformType if any of them are set. (value: 0)

       --useSyN
         Perform a SyN registration as part of the sequential registration
         steps.  This family of options overrides the use of transformType if
         any of them are set. (value: 0)

       --useBSpline
         Perform a BSpline registration as part of the sequential registration
         steps.  This family of options overrides the use of transformType if
         any of them are set. (value: 0)

       --useAffine
         Perform an Affine registration as part of the sequential registration
         steps.  This family of options overrides the use of transformType if
         any of them are set. (value: 0)

       --useScaleSkewVersor3D
         Perform a ScaleSkewVersor3D registration as part of the sequential
         registration steps.  This family of options overrides the use of
         transformType if any of them are set. (value: 0)

       --useScaleVersor3D
         Perform a ScaleVersor3D registration as part of the sequential
         registration steps.  This family of options overrides the use of
         transformType if any of them are set. (value: 0)

       --useRigid
         Perform a rigid registration as part of the sequential registration
         steps.  This family of options overrides the use of transformType if
         any of them are set. (value: 0)

       --initializeTransformMode <Off|useMomentsAlign|useCenterOfHeadAlign
          |useGeometryAlign|useCenterOfROIAlign>
         Determine how to initialize the transform center.  useMomentsAlign
         assumes that the center of mass of the images represent similar
         structures.  useCenterOfHeadAlign attempts to use the top of head and
         shape of neck to drive a center of mass estimate. useGeometryAlign on
         assumes that the center of the voxel lattice of the images represent
         similar structures.  Off assumes that the physical space of the images
         are close.  This flag is mutually exclusive with the Initialization
         transform. (value: Off)

       --initialTransform <std::string>
         Transform to be applied to the moving image to initialize the
         registration.  This can only be used if Initialize Transform Mode is
         Off.

       --outputVolume <std::string>
         (optional) Output image: the moving image warped to the fixed image
         space. NOTE: You must set at least one output object (transform and/or
         output volume).

       --bsplineTransform <std::string>
         (optional) Output estimated transform - in case the computed transform
         is BSpline. NOTE: You must set at least one output object (transform
         and/or output volume).

       --linearTransform <std::string>
         (optional) Output estimated transform - in case the computed transform
         is not BSpline. NOTE: You must set at least one output object
         (transform and/or output volume).

       --splineGridSize <std::vector<int>>
         Number of BSpline grid subdivisions along each axis of the fixed image
         , centered on the image space. Values must be 3 or higher for the
         BSpline to be correctly computed. (value: 14,10,12)

       --samplingPercentage <double>
         Fraction of voxels of the fixed image that will be used for
         registration. The number has to be larger than zero and less or equal
         to one. Higher values increase the computation time but may give more
         accurate results. You can also limit the sampling focus with ROI masks
         and ROIAUTO mask generation. The default is 0.002 (use approximately
         0.2% of voxels, resulting in 100000 samples in a 512x512x192 volume)
         to provide a very fast registration in most cases. Typical values
         range from 0.01 (1%) for low detail images to 0.2 (20%) for high
         detail images. (value: 0.002)

       --movingVolume <std::string>
         Input moving image (this image will be transformed into the fixed
         image space).

       --fixedVolume <std::string>
         Input fixed image (the moving image will be transformed into this
         image space).

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Register a three-dimensional volume to a reference volume
       (Mattes Mutual Information by default). Full documentation avalable
       here:
       http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/BR
       AINSFit. Method described in BRAINSFit: Mutual Information Registrations
       of Whole-Brain 3D Images, Using the Insight Toolkit, Johnson H.J.,
       Harris G., Williams K., The Insight Journal, 2007.
       http://hdl.handle.net/1926/1291

       Author(s): Hans J. Johnson (hans-johnson -at- uiowa.edu,
       http://www.psychiatry.uiowa.edu), Ali Ghayoor

       Acknowledgements: Hans Johnson(1,3,4); Kent Williams(1); Gregory
       Harris(1), Vincent Magnotta(1,2,3);  Andriy Fedorov(5); Ali Ghayoor(4)
       1=University of Iowa Department of Psychiatry, 2=University of Iowa
       Department of Radiology, 3=University of Iowa Department of Biomedical
       Engineering, 4=University of Iowa Department of Electrical and Computer
       Engineering, 5=Surgical Planning Lab, Harvard


### BRAINSLabelStats

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSLabelStats
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--userDefineMaximum <float>]
                                            [--userDefineMinimum <float>]
                                            [--minMaxType <image|label|manual>]
                                            [--numberOfHistogramBins <int>]
                                            [--labelFileType <unknown|fslxml
                                            |ants|csv>]
                                            [--outputPrefixColumnValues
                                            <std::vector<std::string>>]
                                            [--outputPrefixColumnNames
                                            <std::vector<std::string>>]
                                            [--labelNameFile <std::string>]
                                            [--labelVolume <std::string>]
                                            [--imageVolume <std::string>] [--]
                                            [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --userDefineMaximum <float>
         User define maximum value (value: 4095)

       --userDefineMinimum <float>
         User define minimum value (value: 0)

       --minMaxType <image|label|manual>
         Define minimim and maximum values based upon the image, label, or via
         command line (value: image)

       --numberOfHistogramBins <int>
         Number Of Histogram Bins (value: 100000)

       --labelFileType <unknown|fslxml|ants|csv>
         Label File Type (value: unknown)

       --outputPrefixColumnValues <std::vector<std::string>>
         Prefix Column Value(s)

       --outputPrefixColumnNames <std::vector<std::string>>
         Prefix Column Name(s)

       --labelNameFile <std::string>
         Label Name File

       --labelVolume <std::string>
         Label Volume

       --imageVolume <std::string>
         Image Volume

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Compute image statistics within each label of a label
       map.

       Author(s): Vincent A. Magnotta

       Acknowledgements: Funding for this work was provided by the Dana
       Foundation


### BRAINSROIAuto

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSROIAuto
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfThreads <int>]
                                            [--outputVolumePixelType <float
                                            |short|ushort|int|uint|uchar>]
                                            [--ROIAutoDilateSize <double>]
                                            [--closingSize <double>]
                                            [--thresholdCorrectionFactor
                                            <double>]
                                            [--otsuPercentileThreshold
                                            <double>] [--cropOutput]
                                            [--maskOutput] [--outputVolume
                                            <std::string>]
                                            [--outputROIMaskVolume
                                            <std::string>] [--inputVolume
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfThreads <int>
         Explicitly specify the maximum number of threads to use. (value: -1)

       --outputVolumePixelType <float|short|ushort|int|uint|uchar>
         The output image Pixel Type is the scalar datatype for representation
         of the Output Volume. (value: short)

       --ROIAutoDilateSize <double>
         This flag is only relavent when using ROIAUTO mode for initializing
         masks.  It defines the final dilation size to capture a bit of
         background outside the tissue region.  At setting of 10mm has been
         shown to help regularize a BSpline registration type so that there is
         some background constraints to match the edges of the head better.
         (value: 0)

       --closingSize <double>
         The Closing Size (in millimeters) for largest connected filled mask.
         This value is divided by image spacing and rounded to the next largest
         voxel number. (value: 9)

       --thresholdCorrectionFactor <double>
         A factor to scale the Otsu algorithm's result threshold, in case
         clipping mangles the image. (value: 1)

       --otsuPercentileThreshold <double>
         Parameter to the Otsu threshold algorithm. (value: 0.01)

       --cropOutput
         The inputVolume cropped to the region of the ROI mask. (value: 0)

       --maskOutput
         The inputVolume multiplied by the ROI mask. (value: 0)

       --outputVolume <std::string>
         The inputVolume with optional [maskOutput|cropOutput] to the region of
         the brain mask.

       --outputROIMaskVolume <std::string>
         The ROI automatically found from the input image.

       --inputVolume <std::string>
         The input image for finding the largest region filled mask.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This program is used to create a mask over the most
       prominant forground region in an image.  This is accomplished via a
       combination of otsu thresholding and a closing operation.  More
       documentation is available here:
       http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/Fo
       regroundMasking.

       Author(s): Hans J. Johnson, hans-johnson -at- uiowa.edu,
       http://www.psychiatry.uiowa.edu

       Acknowledgements: Hans Johnson(1,3,4); Kent Williams(1); Gregory
       Harris(1), Vincent Magnotta(1,2,3);  Andriy Fedorov(5), fedorov -at-
       bwh.harvard.edu (Slicer integration); (1=University of Iowa Department
       of Psychiatry, 2=University of Iowa Department of Radiology,
       3=University of Iowa Department of Biomedical Engineering, 4=University
       of Iowa Department of Electrical and Computer Engineering, 5=Surgical
       Planning Lab, Harvard)


### BRAINSResample

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSResample
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfThreads <int>]
                                            [--gridSpacing <std::vector<int>>]
                                            [--defaultValue <float>]
                                            [--inverseTransform]
                                            [--interpolationMode
                                            <NearestNeighbor|Linear
                                            |ResampleInPlace|BSpline
                                            |WindowedSinc|Hamming|Cosine|Welch
                                            |Lanczos|Blackman>]
                                            [--warpTransform <std::string>]
                                            [--deformationVolume <std::string>]
                                            [--pixelType <float|short|ushort
                                            |int|uint|uchar|binary>]
                                            [--outputVolume <std::string>]
                                            [--referenceVolume <std::string>]
                                            [--inputVolume <std::string>] [--]
                                            [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfThreads <int>
         Explicitly specify the maximum number of threads to use. (value: -1)

       --gridSpacing <std::vector<int>>
         Add warped grid to output image to help show the deformation that
         occured with specified spacing.   A spacing of 0 in a dimension
         indicates that grid lines should be rendered to fall exactly (i.e. do
         not allow displacements off that plane).  This is useful for makeing a
         2D image of grid lines from the 3D space

       --defaultValue <float>
         Default voxel value (value: 0)

       --inverseTransform
         True/False is to compute inverse of given transformation. Default is
         false (value: 0)

       --interpolationMode <NearestNeighbor|Linear|ResampleInPlace|BSpline
          |WindowedSinc|Hamming|Cosine|Welch|Lanczos|Blackman>
         Type of interpolation to be used when applying transform to moving
         volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline
         , or WindowedSinc (value: Linear)

       --warpTransform <std::string>
         Filename for the BRAINSFit transform (ITKv3 or earlier) or composite
         transform file (ITKv4)

       --deformationVolume <std::string>
         Displacement Field to be used to warp the image (ITKv3 or earlier)

       --pixelType <float|short|ushort|int|uint|uchar|binary>
         Specifies the pixel type for the input/output images.  The 'binary'
         pixel type uses a modified algorithm whereby the image is read in as
         unsigned char, a signed distance map is created, signed distance map
         is resampled, and then a thresholded image of type unsigned char is
         written to disk. (value: float)

       --outputVolume <std::string>
         Resulting deformed image

       --referenceVolume <std::string>
         Reference image used only to define the output space. If not specified
         , the warping is done in the same space as the image to warp.

       --inputVolume <std::string>
         Image To Warp

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This program collects together three common image
       processing tasks that all involve resampling an image volume: Resampling
       to a new resolution and spacing, applying a transformation (using an ITK
       transform IO mechanisms) and Warping (using a vector image deformation
       field).  Full documentation available here:
       http://wiki.slicer.org/slicerWiki/index.php/Documentation/4.1/Modules/BR
       AINSResample.

       Author(s): This tool was developed by Vincent Magnotta, Greg Harris, and
       Hans Johnson.

       Acknowledgements: The development of this tool was supported by funding
       from grants NS050568 and NS40068 from the National Institute of
       Neurological Disorders and Stroke and grants MH31593, MH40856, from the
       National Institute of Mental Health.


### BRAINSResize

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSResize
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--scaleFactor <float>]
                                            [--pixelType <float|short|ushort
                                            |int|uint|uchar|binary>]
                                            [--outputVolume <std::string>]
                                            [--inputVolume <std::string>] [--]
                                            [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --scaleFactor <float>
         The scale factor for the image spacing. (value: 2)

       --pixelType <float|short|ushort|int|uint|uchar|binary>
         Specifies the pixel type for the input/output images.  The 'binary'
         pixel type uses a modified algorithm whereby the image is read in as
         unsigned char, a signed distance map is created, signed distance map
         is resampled, and then a thresholded image of type unsigned char is
         written to disk. (value: float)

       --outputVolume <std::string>
         Resulting scaled image

       --inputVolume <std::string>
         Image To Scale

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This program is useful for downsampling an image by a
       constant scale factor.

       Author(s): This tool was developed by Hans Johnson.

       Acknowledgements: The development of this tool was supported by funding
       from grants NS050568 and NS40068 from the National Institute of
       Neurological Disorders and Stroke and grants MH31593, MH40856, from the
       National Institute of Mental Health.


### BRAINSStripRotation

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSStripRotation
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--transform <std::string>]
                                            [--outputVolume <std::string>]
                                            [--inputVolume <std::string>] [--]
                                            [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --transform <std::string>
         Filename for the transform file

       --outputVolume <std::string>
         Resulting deformed image

       --inputVolume <std::string>
         Image To Warp

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Read an Image, write out same image with identity rotation
       matrix plus an ITK transform file

       Author(s): Kent WIlliams


### BRAINSTransformConvert

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./BRAINSTransformConvert
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--outputTransform <std::string>]
                                            [--displacementVolume
                                            <std::string>]
                                            [--outputPrecisionType <double
                                            |float>] [--outputTransformType
                                            <Affine|VersorRigid|ScaleVersor
                                            |ScaleSkewVersor|DisplacementField
                                            |Same>] [--referenceVolume
                                            <std::string>] [--inputTransform
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --outputTransform <std::string>


       --displacementVolume <std::string>


       --outputPrecisionType <double|float>
         Precision type of the output transform. It can be either single
         precision or double precision (value: double)

       --outputTransformType <Affine|VersorRigid|ScaleVersor|ScaleSkewVersor
          |DisplacementField|Same>
         The target transformation type. Must be conversion-compatible with the
         input transform type (value: Affine)

       --referenceVolume <std::string>


       --inputTransform <std::string>


       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Convert ITK transforms to higher order
       transforms

       Author(s): Hans J. Johnson,Kent Williams, Ali Ghayoor


### CastScalarVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./CastScalarVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-t
                                            <Char|UnsignedChar|Short
                                            |UnsignedShort|Int|UnsignedInt
                                            |Float|Double>] [--] [--version]
                                            [-h] <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -t <Char|UnsignedChar|Short|UnsignedShort|Int|UnsignedInt|Float|Double>,
          --type <Char|UnsignedChar|Short|UnsignedShort|Int|UnsignedInt|Float
          |Double>
         Scalar data type for the new output volume. (value: UnsignedChar)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume, the volume to cast.

       <std::string>
         (required)  Output volume, cast to the new type.


       Description: Cast a volume to a given data type.

       Use at your own risk when casting an input volume into a lower precision
       type!

       Allows casting to the same type as the input volume.

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL,
       BWH)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### CheckerBoardFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./CheckerBoardFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--checkerPattern
                                            <std::vector<int>>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --checkerPattern <std::vector<int>>
         The pattern of input 1 and input 2 in the output image. The user can
         specify the number of checkers in each dimension. A checkerPattern of
         2,2,1 means that images will alternate in every other checker in the
         first two dimensions. The same pattern will be used in the 3rd
         dimension. (value: 2,2,2)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  First Input volume

       <std::string>
         (required)  Second Input volume

       <std::string>
         (required)  Output filtered


       Description: Create a checkerboard volume of two volumes. The output
       volume will show the two inputs alternating according to the user
       supplied checkerPattern. This filter is often used to compare the
       results of image registration. Note that the second input is resampled
       to the same origin, spacing and direction before it is composed with the
       first input. The scalar type of the output volume will be the same as
       the input image scalar type.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### CreateDICOMSeries

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./CreateDICOMSeries
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-t
                                            <UnsignedChar|Char|UnsignedChar
                                            |Short|UnsignedShort|Int
                                            |UnsignedInt>] [--useCompression]
                                            [--reverseImages]
                                            [--dicomNumberFormat <std::string>]
                                            [--dicomPrefix <std::string>]
                                            [--dicomDirectory <std::string>]
                                            [--rescaleSlope <double>]
                                            [--rescaleIntercept <double>]
                                            [--seriesDescription <std::string>]
                                            [--seriesNumber <std::string>]
                                            [--model <std::string>]
                                            [--manufacturer <std::string>]
                                            [--modality <std::string>]
                                            [--studyDescription <std::string>]
                                            [--studyComments <std::string>]
                                            [--studyDate <std::string>]
                                            [--studyID <std::string>]
                                            [--patientComments <std::string>]
                                            [--patientID <std::string>]
                                            [--patientName <std::string>] [--]
                                            [--version] [-h] <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -t <UnsignedChar|Char|UnsignedChar|Short|UnsignedShort|Int|UnsignedInt>,
          --type <UnsignedChar|Char|UnsignedChar|Short|UnsignedShort|Int
          |UnsignedInt>
         Type for the new output volume. (value: Short)

       --useCompression
         Compress the output pixel data. (value: 0)

       --reverseImages
         Reverse the slices. (value: 0)

       --dicomNumberFormat <std::string>
         The printf-style format to be used when creating the per-slice DICOM
         filename. (value: %04d)

       --dicomPrefix <std::string>
         The prefix of the DICOM filename. (value: IMG)

       --dicomDirectory <std::string>
         The directory to contain the DICOM series. (value: ./)

       --rescaleSlope <double>
         Rescale slope [0028-1053]. Converts pixel values on disk to pixel
         values in memory. (Pixel value in memory) = (Pixel value on disk) *
         rescaleSlope + rescaleInterscept.  Default is 1.0. Data values are
         converted on write (the data is scaled and shifted so that the slope
         and interscept will bring it back to the current intensity range).
         (value: 1)

       --rescaleIntercept <double>
         Rescale interscept [0028-1052]. Converts pixel values on disk to pixel
         values in memory. (Pixel value in memory) = (Pixel value on disk) *
         rescaleSlope + rescaleIntercept.  Default is 0.0. Data values are
         converted on write (the data is scaled and shifted so that the slope
         and interscept will bring it back to the current intensity range).
         (value: 0)

       --seriesDescription <std::string>
         Series description [0008-103E] (value: None)

       --seriesNumber <std::string>
         The series number [0020-0011] (value: 123456)

       --model <std::string>
         model [0008-1090] (value: None)

       --manufacturer <std::string>
         Manufacturer [0008-0070] (value: GE Medical Systems)

       --modality <std::string>
         Modality [0008-0060] (value: CT)

       --studyDescription <std::string>
         Study description[0008-1030] (value: None)

       --studyComments <std::string>
         Study comments[0032-4000] (value: None)

       --studyDate <std::string>
         The date of the study [0008-0020] (value: 20060101)

       --studyID <std::string>
         The study ID [0020-0010] (value: 123456)

       --patientComments <std::string>
         Patient comments [0010-4000] (value: None)

       --patientID <std::string>
         The patient ID [0010-0020] (value: 123456)

       --patientName <std::string>
         The name of the patient [0010-0010] (value: Anonymous)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be resampled


       Description: Create a DICOM Series from a Slicer volume. User can
       specify values for selected DICOM tags in the UI. Given the number of
       tags DICOM series have, it is impossible to expose all tags in UI. So
       only important tags can be set by the user.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from Insight/Examples
       (copyright) Insight Software Consortium


### CurvatureAnisotropicDiffusion

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./CurvatureAnisotropicDiffusion
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--timeStep <double>] [--iterations
                                            <int>] [--conductance <double>]
                                            [--] [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --timeStep <double>
         Time Step (value: 0.0625)

       --iterations <int>
         The more iterations, the more smoothing. Each iteration takes the same
         amount of time. If it takes 10 seconds for one iteration, then it will
         take 100 seconds for 10 iterations. Note that the conductance controls
         how much each iteration smooths across edges. (value: 1)

       --conductance <double>
         Conductance (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: Performs anisotropic diffusion on an image using a modified
       curvature diffusion equation (MCDE).



       MCDE does not exhibit the edge enhancing properties of classic
       anisotropic diffusion, which can under certain conditions undergo a
       'negative' diffusion, which enhances the contrast of edges.  Equations
       of the form of MCDE always undergo positive diffusion, with the
       conductance term only varying the strength of that diffusion.



       Qualitatively, MCDE compares well with other non-linear diffusion
       techniques.  It is less sensitive to contrast than classic Perona-Malik
       style diffusion, and preserves finer detailed structures in images.
       There is a potential speed trade-off for using this function in place of
       Gradient Anisotropic Diffusion.  Each iteration of the solution takes
       roughly twice as long.  Fewer iterations, however, may be required to
       reach an acceptable solution.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from Insight/Examples
       (copyright) Insight Software Consortium


### DWIConvert

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./DWIConvert
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--fMRI] [--gradientVectorFile
                                            <std::string>]
                                            [--allowLossyConversion]
                                            [--transposeInputBVectors]
                                            [--smallGradientThreshold <double>]
                                            [--outputDirectory <std::string>]
                                            [--useBMatrixGradientDirections]
                                            [--useIdentityMeaseurementFrame]
                                            [--writeProtocolGradientsFile]
                                            [--outputBVectors <std::string>]
                                            [--outputBValues <std::string>]
                                            [--outputNiftiFile <std::string>]
                                            [--inputBVectors <std::string>]
                                            [--inputBValues <std::string>]
                                            [--fslNIFTIFile <std::string>] [-i
                                            <std::string>] [-o <std::string>]
                                            [--inputVolume <std::string>]
                                            [--conversionMode <DicomToNrrd
                                            |DicomToFSL|NrrdToFSL|FSLToNrrd>]
                                            [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --fMRI
         DEPRECATED:  No support or testing.  Output a NRRD file, but without
         gradients

       --gradientVectorFile <std::string>
         DEPRECATED:  Use --inputBVector --inputBValue files Text file giving
         gradient vectors

       --allowLossyConversion
         The only supported output type is 'short'. Conversion from images of a
         different type may cause data loss due to rounding or truncation. Use
         with caution!' (value: 0)

       --transposeInputBVectors
         FSL input BVectors are expected to be encoded in the input file as one
         vector per line. If it is not the case, use this option to transpose
         the file as it is read (value: 0)

       --smallGradientThreshold <double>
         If a gradient magnitude is greater than 0 and less than
         smallGradientThreshold, then DWIConvert will display an error message
         and quit, unless the useBMatrixGradientDirections option is set.
         (value: 0.2)

       --outputDirectory <std::string>
         Directory holding the output NRRD file (value: .)

       --useBMatrixGradientDirections
         Fill the nhdr header with the gradient directions and bvalues computed
         out of the BMatrix. Only changes behavior for Siemens data.  In some
         cases the standard public gradients are not properly computed.  The
         gradients can emperically computed from the private BMatrix fields.
         In some cases the private BMatrix is consistent with the public
         grandients, but not in all cases, when it exists BMatrix is usually
         most robust. (value: 0)

       --useIdentityMeaseurementFrame
         Adjust all the gradients so that the measurement frame is an identity
         matrix. (value: 0)

       --writeProtocolGradientsFile
         Write the protocol gradients to a file suffixed by '.txt' as they were
         specified in the procol by multiplying each diffusion gradient
         direction by the measurement frame.  This file is for debugging
         purposes only, the format is not fixed, and will likely change as
         debugging of new dicom formats is necessary. (value: 0)

       --outputBVectors <std::string>
         The Gradient Vectors are stored in FSL .bvec text file format
         (defaults to <outputVolume>.bvec)

       --outputBValues <std::string>
         The B Values are stored in FSL .bval text file format (defaults to
         <outputVolume>.bval)

       --outputNiftiFile <std::string>
         Nifti output filename (for Slicer GUI use).

       --inputBVectors <std::string>
         The Gradient Vectors are stored in FSL .bvec text file format

       --inputBValues <std::string>
         The B Values are stored in FSL .bval text file format

       --fslNIFTIFile <std::string>
         4D NIfTI file containing gradient volumes

       -i <std::string>,  --inputDicomDirectory <std::string>
         Directory holding Dicom series

       -o <std::string>,  --outputVolume <std::string>
         Output filename (.nhdr or .nrrd)

       --inputVolume <std::string>
         Input DWI volume -- not used for DicomToNrrd mode.

       --conversionMode <DicomToNrrd|DicomToFSL|NrrdToFSL|FSLToNrrd>
         Determine which conversion to perform. DicomToNrrd (default): Convert
         DICOM series to NRRD DicomToFSL: Convert DICOM series to NIfTI File +
         gradient/bvalue text files NrrdToFSL: Convert DWI NRRD file to NIfTI
         File + gradient/bvalue text files FSLToNrrd: Convert NIfTI File +
         gradient/bvalue text files to NRRD file. (value: DicomToNrrd)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Converts diffusion weighted MR images in DICOM series into
       NRRD format for analysis in Slicer. This program has been tested on only
       a limited subset of DTI DICOM formats available from Siemens, GE, and
       Philips scanners. Work in progress to support DICOM multi-frame data.
       The program parses DICOM header to extract necessary information about
       measurement frame, diffusion weighting directions, b-values, etc, and
       write out a NRRD image. For non-diffusion weighted DICOM images, it
       loads in an entire DICOM series and writes out a single dicom volume in
       a .nhdr/.raw pair.

       Author(s): Hans Johnson (UIowa), Vince Magnotta (UIowa) Joy Matsui
       (UIowa), Kent Williams (UIowa), Mark Scully (Uiowa), Xiaodong Tao
       (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.
       Additional support for DTI data produced on Philips scanners was
       contributed by Vincent Magnotta and Hans Johnson at the University of
       Iowa.


### EMSegmentCommandLine

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./EMSegmentCommandLine
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--registrationDeformableType
                                            <int>] [--registrationAffineType
                                            <int>] [--registrationPackage
                                            <std::string>]
                                            [--atlasVolumeFileNames
                                            <std::vector<std::string>>] ...
                                            [--disableCompression]
                                            [--resultMRMLSceneFileName
                                            <std::string>]
                                            [--generateEmptyMRMLSceneAndQuit
                                            <std::string>] [--dontWriteResults]
                                            [--resultStandardVolumeFileName
                                            <std::string>]
                                            [--autoBoundaryDetection]
                                            [--keepTempFiles]
                                            [--taskPreProcessingSetting
                                            <std::string>]
                                            [--loadAtlasCentered]
                                            [--loadTargetCentered] [--verbose]
                                            [--dontUpdateIntermediateData
                                            <int>] [--disableMultithreading
                                            <int>] [--parametersMRMLNodeName
                                            <std::string>]
                                            [--writeIntermediateResults]
                                            [--intermediateResultsDirectory
                                            <std::string>]
                                            [--targetVolumeFileNames
                                            <std::vector<std::string>>] ...
                                            [--resultVolumeFileName
                                            <std::string>] [--mrmlSceneFileName
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --registrationDeformableType <int>
         specify the accuracy of the deformable registration. -2: Do not
         overwrite default, -1: Test, 0: Disable, 1: Fast, 2: Accurate (value:
         -2)

       --registrationAffineType <int>
         specify the accuracy of the affine registration. -2: Do not overwrite
         default, -1: Test, 0: Disable, 1: Fast, 2: Accurate (value: -2)

       --registrationPackage <std::string>
         specify the registration package for preprocessing (CMTK or BRAINS or
         PLASTIMATCH or DEMONS)

       --atlasVolumeFileNames <std::vector<std::string>>  (accepted multiple
          times)
         Use an alternative atlas to the one that is specified by the mrml file
         - note the order matters !

       --disableCompression
         Don't use compression when writing result image to disk. (value: 0)

       --resultMRMLSceneFileName <std::string>
         Write out the MRML scene after command line substitutions have been
         made.

       --generateEmptyMRMLSceneAndQuit <std::string>
         Used for testing.  Only write a scene with default mrml parameters.

       --dontWriteResults
         Used for testing.  Don't actually write the resulting labelmap to
         disk. (value: 0)

       --resultStandardVolumeFileName <std::string>
         Used for testing.  Compare segmentation results to this image and
         return EXIT_FAILURE if they do not match.

       --autoBoundaryDetection
         If flag is set then the method will automatically determine the
         boundary box which includes non-zero voxels in the input images. This
         speed things up when working with skull stripped images (value: 0)

       --keepTempFiles
         If flag is set then at the end of command the temporary files are not
         removed (value: 0)

       --taskPreProcessingSetting <std::string>
         Specifies the different task parameter. Leave blank for default.

       --loadAtlasCentered
         Read atlas files centered. (value: 0)

       --loadTargetCentered
         Read target files centered. (value: 0)

       --verbose
         Enable verbose output. (value: 0)

       --dontUpdateIntermediateData <int>
         Disable update of intermediate results.  -1: Do not overwrite default
         value. 0: Disable. 1: Enable. (value: -1)

       --disableMultithreading <int>
         Disable multithreading for the EMSegmenter algorithm only!
         Preprocessing might still run in multi-threaded mode. -1: Do not
         overwrite default value. 0: Disable. 1: Enable. (value: -1)

       --parametersMRMLNodeName <std::string>
         The name of the EMSegment parameters node within the active MRML
         scene.  Leave blank for default.

       --writeIntermediateResults
         Write out intermediate data (e.g., aligned atlas data). (value: 0)

       --intermediateResultsDirectory <std::string>
         write intermediate data (e.g., aligned atlas data).

       --targetVolumeFileNames <std::vector<std::string>>  (accepted multiple
          times)
         File names of target volumes (to be segmented).  The number of target
         images must be equal to the number of target images specified in the
         parameter set, and these images must be spatially aligned.

       --resultVolumeFileName <std::string>
         The file name that the segmentation result volume will be written to.

       --mrmlSceneFileName <std::string>
         Active MRML scene that contains EMSegment algorithm parameters.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This module is used to simplify the process of segmenting
       large collections of images by providing a command line interface to the
       EMSegment algorithm for script and batch processing.

       Author(s): Sebastien Barre, Brad Davis, Kilian Pohl, Polina Golland,
       Yumin Yuan, Daniel Haehn

       Acknowledgements: Many people and organizations have contributed to the
       funding, design, and development of the EMSegment algorithm and its
       various implementations.


### EMSegmentTransformToNewFormat

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./EMSegmentTransformToNewFormat
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-t]
                                            [-o <std::string>] [-i
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -t,  --templateFlag
         Set to true if the transformed mrml file should be used as template
         file (value: 0)

       -o <std::string>,  --outputMRMLFileName <std::string>
         Write out the MRML scene after transformation to format 3.6.3 has been
         made. - has to be in the same directory as the input MRML file due to
         Slicer Core bug  - please include absolute  file name in path

       -i <std::string>,  --inputMRMLFileName <std::string>
         Active MRML scene that contains EMSegment algorithm parameters in the
         format before 3.6.3 - please include absolute  file name in path.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Transform MRML Files to New EMSegmenter Standard

       Author(s): Anonymous

       Acknowledgements: Thank you everyone.


### ExecutionModelTour

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ExecutionModelTour
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--outputDT <std::string>]
                                            [--inputDT <std::string>]
                                            [--outputFA <std::string>]
                                            [--inputFA <std::string>] [--region
                                            <std::vector<std::vector<float> >>]
                                            ...  [--modelSceneFile
                                            <std::string>] ...  [--outputModel
                                            <std::string>] [--inputModel
                                            <std::string>] [--seedsOutFile
                                            <std::string>] [--seedsFile
                                            <std::string>] [--seed
                                            <std::vector<std::vector<float> >>]
                                            ...  [--transformOutputBspline
                                            <std::string>]
                                            [--transformOutputNonlinear
                                            <std::string>] [--transform2
                                            <std::string>] [--transformOutput
                                            <std::string>]
                                            [--transformInputBspline
                                            <std::string>]
                                            [--transformInputNonlinear
                                            <std::string>] [--transform1
                                            <std::string>] [--transformInput
                                            <std::string>] [--image2
                                            <std::string>] [--image1
                                            <std::string>] [--directory1
                                            <std::string>] [--outputFile1
                                            <std::string>] [--files
                                            <std::vector<std::string>>] ...
                                            [--file1 <std::string>]
                                            [--boolean3] [--boolean2]
                                            [--boolean1] [-e <Ron|Eric|Bill
                                            |Ross|Steve|Will>] [--string_vector
                                            <std::vector<std::string>>] [-f
                                            <std::vector<float>>] [-d <double>]
                                            [-i <int>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --outputDT <std::string>
         Array of processed (output) Table values

       --inputDT <std::string>
         Array of Table values to process

       --outputFA <std::string>
         Array of processed (output) FA values

       --inputFA <std::string>
         Array of FA values to process

       --region <std::vector<std::vector<float> >>  (accepted multiple times)
         List of regions to process

       --modelSceneFile <std::string>  (accepted multiple times)
         Generated models, under a model hierarchy node. Models are imported
         into Slicer under a model hierarchy node. The model hierarchy node
         must be created before running the model maker, by selecting Create
         New ModelHierarchy from the Models drop down menu. (value: None)

       --outputModel <std::string>
         Output model

       --inputModel <std::string>
         Input model

       --seedsOutFile <std::string>
         Output file to read back in, compare to seeds with flipped settings on
         first fiducial

       --seedsFile <std::string>
         Test file of input fiducials, compared to seeds

       --seed <std::vector<std::vector<float> >>  (accepted multiple times)
         Lists of points in the CLI correspond to slicer fiducial lists (value:
         None)

       --transformOutputBspline <std::string>
         A bspline output transform

       --transformOutputNonlinear <std::string>
         A nonlinear output transform

       --transform2 <std::string>
         A linear output transform

       --transformOutput <std::string>
         A generic output transform

       --transformInputBspline <std::string>
         A bspline input transform

       --transformInputNonlinear <std::string>
         A nonlinear input transform

       --transform1 <std::string>
         A linear input transform

       --transformInput <std::string>
         A generic input transform

       --image2 <std::string>
         An output image

       --image1 <std::string>
         An input image

       --directory1 <std::string>
         An input directory. If no default is specified, the current directory
         is used,

       --outputFile1 <std::string>
         An output file

       --files <std::vector<std::string>>  (accepted multiple times)
         Multiple input files

       --file1 <std::string>
         An input file

       --boolean3
         A boolean with no default, should be defaulting to false

       --boolean2
         A boolean default false (value: 0)

       --boolean1
         A boolean default true (value: 0)

       -e <Ron|Eric|Bill|Ross|Steve|Will>,  --enumeration <Ron|Eric|Bill|Ross
          |Steve|Will>
         An enumeration of strings (value: Bill)

       --string_vector <std::vector<std::string>>
         A vector of strings (value: foo,bar,foobar)

       -f <std::vector<float>>,  -- <std::vector<float>>
         A vector of floats (value: 1.3,2,-14)

       -d <double>,  --double <double>
         A double with constraints (value: 30)

       -i <int>,  --integer <int>
         An integer without constraints (value: 30)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  First index argument is an image

       <std::string>
         (required)  Second index argument is an image


       Description: Shows one of each type of parameter.

       Author(s): Daniel Blezek (GE), Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ExpertAutomatedRegistration

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ExpertAutomatedRegistration
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--controlPointSpacing <int>]
                                            [--bsplineSamplingRatio <float>]
                                            [--bsplineMaxIterations <int>]
                                            [--affineSamplingRatio <float>]
                                            [--affineMaxIterations <int>]
                                            [--rigidSamplingRatio <float>]
                                            [--rigidMaxIterations <int>]
                                            [--movingLandmarks
                                            <std::vector<std::vector<float> >>]
                                            ...  [--fixedLandmarks
                                            <std::vector<std::vector<float> >>]
                                            ...  [--interpolation
                                            <NearestNeighbor|Linear|BSpline>]
                                            [--minimizeMemory]
                                            [--numberOfThreads <int>]
                                            [--randomNumberSeed <int>]
                                            [--fixedImageMask <std::string>]
                                            [--sampleFromOverlap]
                                            [--verbosityLevel <Silent|Standard
                                            |Verbose>] [--expectedSkew <float>]
                                            [--expectedScale <float>]
                                            [--expectedRotation <float>]
                                            [--expectedOffset <float>]
                                            [--metric <MattesMI|NormCorr
                                            |MeanSqrd>] [--registration <None
                                            |Initial|Rigid|Affine|BSpline
                                            |PipelineRigid|PipelineAffine
                                            |PipelineBSpline>]
                                            [--initialization <None|Landmarks
                                            |ImageCenters|CentersOfMass
                                            |SecondMoments>] [--saveTransform
                                            <std::string>] [--loadTransform
                                            <std::string>] [--resampledImage
                                            <std::string>] [--] [--version]
                                            [-h] <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --controlPointSpacing <int>
         Number of pixels between control points (value: 40)

       --bsplineSamplingRatio <float>
         Portion of the image to use in computing the metric during BSpline
         registration (value: 0.1)

       --bsplineMaxIterations <int>
         Maximum number of bspline optimization iterations (value: 20)

       --affineSamplingRatio <float>
         Portion of the image to use in computing the metric during affine
         registration (value: 0.02)

       --affineMaxIterations <int>
         Maximum number of affine optimization iterations (value: 50)

       --rigidSamplingRatio <float>
         Portion of the image to use in computing the metric during rigid
         registration (value: 0.01)

       --rigidMaxIterations <int>
         Maximum number of rigid optimization iterations (value: 100)

       --movingLandmarks <std::vector<std::vector<float> >>  (accepted multiple
          times)
         Ordered list of landmarks in the moving image

       --fixedLandmarks <std::vector<std::vector<float> >>  (accepted multiple
          times)
         Ordered list of landmarks in the fixed image

       --interpolation <NearestNeighbor|Linear|BSpline>
         Method for interpolation within the optimization process (value:
         Linear)

       --minimizeMemory
         Reduce the amount of memory required at the cost of increased
         computation time (value: 0)

       --numberOfThreads <int>
         Number of CPU threads to use (value: 0)

       --randomNumberSeed <int>
         Seed to generate a consistent random number sequence (value: 0)

       --fixedImageMask <std::string>
         Image which defines a mask for the fixed image

       --sampleFromOverlap
         Limit metric evaluation to the fixed image region overlapped by the
         moving image (value: 0)

       --verbosityLevel <Silent|Standard|Verbose>
         Level of detail of reporting progress (value: Standard)

       --expectedSkew <float>
         Expected misalignment after initialization (value: 0.01)

       --expectedScale <float>
         Expected misalignment after initialization (value: 0.05)

       --expectedRotation <float>
         Expected misalignment after initialization (value: 0.1)

       --expectedOffset <float>
         Expected misalignment after initialization (value: 10)

       --metric <MattesMI|NormCorr|MeanSqrd>
         Method to quantify image match (value: MattesMI)

       --registration <None|Initial|Rigid|Affine|BSpline|PipelineRigid
          |PipelineAffine|PipelineBSpline>
         Method for the registration process (value: PipelineAffine)

       --initialization <None|Landmarks|ImageCenters|CentersOfMass
          |SecondMoments>
         Method to prime the registration process (value: CentersOfMass)

       --saveTransform <std::string>
         Save the transform that results from registration

       --loadTransform <std::string>
         Load a transform that is immediately applied to the moving image

       --resampledImage <std::string>
         Registration results

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Image which defines the space into which the moving image
         is registered

       <std::string>
         (required)  The transform goes from the fixed image's space into the
         moving image's space


       Description: Provides rigid, affine, and BSpline registration methods
       via a simple GUI

       Author(s): Stephen R Aylward (Kitware), Casey B Goodlett
       (Kitware)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ExtractSkeleton

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ExtractSkeleton
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--pointsFile <std::string>]
                                            [--numPoints <int>] [--dontPrune]
                                            [--type <1D|2D>] [--] [--version]
                                            [-h] <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --pointsFile <std::string>
         Name of the file to store the coordinates of the central (1D) skeleton
         points (value: skeleton.txt)

       --numPoints <int>
         Number of points used to represent the skeleton (value: 100)

       --dontPrune
         Return the full skeleton, not just the maximal skeleton (value: 0)

       --type <1D|2D>
         Type of skeleton to create (value: 1D)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input image

       <std::string>
         (required)  Skeleton of the input image


       Description: Extract the skeleton of a binary object.  The skeleton can
       be limited to being a 1D curve or allowed to be a full 2D manifold.  The
       branches of the skeleton can be pruned so that only the maximal center
       skeleton is returned.

       Author(s): Pierre Seroul (UNC), Martin Styner (UNC), Guido Gerig (UNC),
       Stephen Aylward (Kitware)

       Acknowledgements: The original implementation of this method was
       provided by ETH Zurich, Image Analysis Laboratory of Profs Olaf Kuebler,
       Gabor Szekely and Guido Gerig.  Martin Styner at UNC, Chapel Hill made
       enhancements.  Wrapping for Slicer was provided by Pierre Seroul and
       Stephen Aylward at Kitware, Inc.


### FiducialRegistration

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./FiducialRegistration
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--transformType <Translation|Rigid
                                            |Similarity>] [--saveTransform
                                            <std::string>] [--movingLandmarks
                                            <std::vector<std::vector<float> >>]
                                            ...  [--fixedLandmarks
                                            <std::vector<std::vector<float> >>]
                                            ...  [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --transformType <Translation|Rigid|Similarity>
         Type of transform to produce (value: Rigid)

       --saveTransform <std::string>
         Save the transform that results from registration

       --movingLandmarks <std::vector<std::vector<float> >>  (accepted multiple
          times)
         Ordered list of landmarks in the moving image

       --fixedLandmarks <std::vector<std::vector<float> >>  (accepted multiple
          times)
         Ordered list of landmarks in the fixed image

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Computes a rigid, similarity or affine transform from a
       matched list of fiducials

       Author(s): Casey B Goodlett (Kitware), Dominik Meier (SPL,
       BWH)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### GaussianBlurImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./GaussianBlurImageFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-s
                                            <double>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -s <double>,  --sigma <double>
         Sigma value in physical units (e.g., mm) of the Gaussian kernel
         (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume

       <std::string>
         (required)  Blurred Volume


       Description: Apply a gaussian blurr to an image

       Author(s): Julien Jomier (Kitware), Stephen Aylward
       (Kitware)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### GradientAnisotropicDiffusion

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./GradientAnisotropicDiffusion
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--useImageSpacing] [--timeStep
                                            <double>] [--iterations <int>]
                                            [--conductance <double>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --useImageSpacing
         ![CDATA[Take into account image spacing in the computation.  It is
         advisable to turn this option on, especially when the pixel size is
         different in different dimensions. However, to produce results
         consistent with Slicer4.2 and earlier, this option should be turned
         off.]] (value: 0)

       --timeStep <double>
         The time step depends on the dimensionality of the image. In Slicer
         the images are 3D and the default (.0625) time step will provide a
         stable solution. (value: 0.0625)

       --iterations <int>
         The more iterations, the more smoothing. Each iteration takes the same
         amount of time. If it takes 10 seconds for one iteration, then it will
         take 100 seconds for 10 iterations. Note that the conductance controls
         how much each iteration smooths across edges. (value: 5)

       --conductance <double>
         Conductance controls the sensitivity of the conductance term. As a
         general rule, the lower the value, the more strongly the filter
         preserves edges. A high value will cause diffusion (smoothing) across
         edges. Note that the number of iterations controls how much smoothing
         is done within regions bounded by edges. (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: Runs gradient anisotropic diffusion on a
       volume.



       Anisotropic diffusion methods reduce noise (or unwanted detail) in
       images while preserving specific image features, like edges.  For many
       applications, there is an assumption that light-dark transitions (edges)
       are interesting.  Standard isotropic diffusion methods move and blur
       light-dark boundaries.  Anisotropic diffusion methods are formulated to
       specifically preserve edges. The conductance term for this
       implementation is a function of the gradient magnitude of the image at
       each point, reducing the strength of diffusion at edges. The numerical
       implementation of this equation is similar to that described in the
       Perona-Malik paper, but uses a more robust technique for gradient
       magnitude estimation and has been generalized to
       N-dimensions.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from Insight/Examples
       (copyright) Insight Software Consortium


### GrayscaleFillHoleImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./GrayscaleFillHoleImageFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: GrayscaleFillholeImageFilter fills holes in a grayscale
       image.  Holes are local minima in the grayscale topography that are not
       connected to boundaries of the image. Gray level values adjacent to a
       hole are extrapolated across the hole.



       This filter is used to smooth over local minima without affecting the
       values of local maxima.  If you take the difference between the output
       of this filter and the original image (and perhaps threshold the
       difference above a small value), you'll obtain a map of the local
       minima.



       This filter uses the itkGrayscaleGeodesicErodeImageFilter.  It provides
       its own input as the 'mask' input to the geodesic erosion.  The 'marker'
       image for the geodesic erosion is constructed such that boundary pixels
       match the boundary pixels of the input image and the interior pixels are
       set to the maximum pixel value in the input image.



       Geodesic morphology and the Fillhole algorithm is described in Chapter 6
       of Pierre Soille's book 'Morphological Image Analysis: Principles and
       Applications', Second Edition, Springer, 2003.



       A companion filter, Grayscale Grind Peak, removes peaks in grayscale
       images.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### GrayscaleGrindPeakImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./GrayscaleGrindPeakImageFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: GrayscaleGrindPeakImageFilter removes peaks in a grayscale
       image. Peaks are local maxima in the grayscale topography that are not
       connected to boundaries of the image. Gray level values adjacent to a
       peak are extrapolated through the peak.



       This filter is used to smooth over local maxima without affecting the
       values of local minima.  If you take the difference between the output
       of this filter and the original image (and perhaps threshold the
       difference above a small value), you'll obtain a map of the local
       maxima.



       This filter uses the GrayscaleGeodesicDilateImageFilter.  It provides
       its own input as the 'mask' input to the geodesic erosion.  The 'marker'
       image for the geodesic erosion is constructed such that boundary pixels
       match the boundary pixels of the input image and the interior pixels are
       set to the minimum pixel value in the input image.



       This filter is the dual to the GrayscaleFillholeImageFilter which
       implements the Fillhole algorithm.  Since it is a dual, it is somewhat
       superfluous but is provided as a convenience.



       Geodesic morphology and the Fillhole algorithm is described in Chapter 6
       of Pierre Soille's book 'Morphological Image Analysis: Principles and
       Applications', Second Edition, Springer, 2003.



       A companion filter, Grayscale Fill Hole, fills holes in grayscale
       images.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### GrayscaleModelMaker

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./GrayscaleModelMaker
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--pointnormals] [--splitnormals]
                                            [--decimate <float>] [--smooth
                                            <int>] [-n <std::string>] [-t
                                            <float>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --pointnormals
         Calculate the point normals? Calculated point normals make the surface
         appear smooth. Without point normals, the surface will appear faceted.
         (value: 0)

       --splitnormals
         Splitting normals is useful for visualizing sharp features. However it
         creates holes in surfaces which affect measurements (value: 0)

       --decimate <float>
         Target reduction during decimation, as a decimal percentage reduction
         in the number of polygons. If 0, no decimation will be done. (value:
         0.25)

       --smooth <int>
         Number of smoothing iterations. If 0, no smoothing will be done.
         (value: 15)

       -n <std::string>,  --name <std::string>
         Name to use for this model. (value: Model)

       -t <float>,  --threshold <float>
         Grayscale threshold of isosurface. The resulting surface of triangles
         separates the volume into voxels that lie above (inside) and below
         (outside) the threshold. (value: 100)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Volume containing the input grayscale data.

       <std::string>
         (required)  Output that contains geometry model.


       Description: Create 3D surface models from grayscale data. This module
       uses Marching Cubes to create an isosurface at a given threshold. The
       resulting surface consists of triangles that separate a volume into
       regions below and above the threshold. The resulting surface can be
       smoothed and decimated. This model works on continuous data while the
       module Model Maker works on labeled (or discrete) data.

       Author(s): Nicole Aucoin (SPL, BWH), Bill Lorensen
       (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### HistogramMatching

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./HistogramMatching
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--threshold]
                                            [--numberOfMatchPoints <int>]
                                            [--numberOfHistogramLevels <int>]
                                            [--] [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --threshold
         If on, only pixels above the mean in each volume are thresholded.
         (value: 0)

       --numberOfMatchPoints <int>
         The number of match points to use (value: 10)

       --numberOfHistogramLevels <int>
         The number of hisogram levels to use (value: 128)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Input volume whose histogram will be matched

       <std::string>
         (required)  Output volume. This is the input volume with intensities
         matched to the reference volume.


       Description: Normalizes the grayscale values of a source image based on
       the grayscale values of a reference image.  This filter uses a histogram
       matching technique where the histograms of the two images are matched
       only at a specified number of quantile values.



       The filter was orginally designed to normalize MR images of the sameMR
       protocol and same body part. The algorithm works best if background
       pixels are excluded from both the source and reference histograms.  A
       simple background exclusion method is to exclude all pixels whose
       grayscale values are smaller than the mean grayscale value.
       ThresholdAtMeanIntensity switches on this simple background exclusion
       method.



       Number of match points governs the number of quantile values to be
       matched.



       The filter assumes that both the source and reference are of the same
       type and that the input and output image type have the same number of
       dimension and have scalar pixel types.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ImageLabelCombine

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ImageLabelCombine
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-f]
                                            [--] [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -f,  --first_overwrites
         Use first or second label when both are present (value: 0)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Label map image

       <std::string>
         (required)  Label map image

       <std::string>
         (required)  Resulting Label map image


       Description: Combine two label maps into one

       Author(s): Alex Yarmarkovich (SPL, BWH)


### IslandRemoval

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./IslandRemoval
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-n]
                                            [-m <int>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -n,  --neighborhood2D
         If set then uses 2D instead of 3D neighborhood to define connectivity.
         (value: 0)

       -m <int>,  --min <int>
         Islands smaller than this size will be removed. (value: 10)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Volume containing the input label map.

       <std::string>
         (required)  Label map with islands removed.


       Description: Removes island smaller than threshold by assigning them to
       the label associated with the majority of neighboring voxels.

       Author(s): Kilian M Pohl (SRI/Stanford)


### LabelMapSmoothing

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./LabelMapSmoothing
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--gaussianSigma <float>]
                                            [--maxRMSError <float>]
                                            [--numberOfIterations <int>]
                                            [--labelToSmooth <int>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --gaussianSigma <float>
         The standard deviation of the Gaussian kernel (value: 0.2)

       --maxRMSError <float>
         The maximum RMS error. (value: 0.01)

       --numberOfIterations <int>
         The number of iterations of the level set AntiAliasing algorithm
         (value: 50)

       --labelToSmooth <int>
         The label to smooth.  All others will be ignored.  If no label is
         selected by the user, the maximum label in the image is chosen by
         default. (value: -1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input label map to smooth

       <std::string>
         (required)  Smoothed label map


       Description: This filter smoothes a binary label map.  With a label map
       as input, this filter runs an anti-alising algorithm followed by a
       Gaussian smoothing algorithm.  The output is a smoothed label
       map.

       Author(s): Dirk Padfield (GE), Josh Cates (Utah), Ross Whitaker
       (Utah)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.  This
       filter is based on work developed at the University of Utah, and
       implemented at GE Research.


### MaskScalarVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./MaskScalarVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-r
                                            <int>] [-l <int>] [--] [--version]
                                            [-h] <std::string> <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -r <int>,  --replace <int>
         Value to use for the output volume outside of the mask (value: 0)

       -l <int>,  --label <int>
         Label value in the Mask Volume to use as the mask (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be masked

       <std::string>
         (required)  Label volume containing the mask

       <std::string>
         (required)  Output volume: Input Volume masked by label value from
         Mask Volume


       Description: Masks two images. The output image is set to 0 everywhere
       except where the chosen label from the mask volume is present, at which
       point it will retain it's original values. The two images do not have to
       have the same dimensions.

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL,
       BWH)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### MedianImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./MedianImageFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--neighborhood <std::vector<int>>]
                                            [--] [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --neighborhood <std::vector<int>>
         The size of the neighborhood in each dimension (value: 1,1,1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: The MedianImageFilter is commonly used as a robust approach
       for noise reduction. This filter is particularly efficient against
       'salt-and-pepper' noise. In other words, it is robust to the presence of
       gray-level outliers. MedianImageFilter computes the value of each output
       pixel as the statistical median of the neighborhood of values around the
       corresponding input pixel.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from
       Insight/Examples/Filtering/MedianImageFilter (copyright) Insight
       Software Consortium


### MergeModels

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./MergeModels
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input model 1

       <std::string>
         (required)  Input model 2

       <std::string>
         (required)  Output model


       Description: Merge the polydata from two input models and output a new
       model with the combined polydata. Uses the vtkAppendPolyData filter.
       Works on .vtp and .vtk surface files.

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH), Daniel
       Haehn (SPL, BWH, UPenn)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ModelMaker

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ModelMaker
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-d]
                                            [--saveIntermediateModels]
                                            [--modelHierarchyFile
                                            <std::string>] [--pad]
                                            [--pointnormals] [--splitnormals]
                                            [--decimate <float>] [--filtertype
                                            <Sinc|Laplacian>] [--smooth <int>]
                                            [-j] [--skipUnNamed] [-e <int>] [-s
                                            <int>] [-l <std::vector<int>>]
                                            [--generateAll] [-n <std::string>]
                                            [--modelSceneFile <std::string>]
                                            ...  [--color <std::string>] [--]
                                            [--version] [-h] <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -d,  --debug
         turn this flag on in order to see debugging output (look in the Error
         Log window that is accessed via the View menu) (value: 0)

       --saveIntermediateModels
         You can save a copy of the models after each of the intermediate steps
         (marching cubes, smoothing, and decimation if not joint smoothing,
         otherwise just after decimation). These intermediate models are not
         saved in the mrml file, you have to load them manually after turning
         off deleting temporary files in they python console (View ->Python
         Interactor) using the following command
         slicer.modules.modelmaker.cliModuleLogic().DeleteTemporaryFilesOff().
         (value: 0)

       --modelHierarchyFile <std::string>
         A mrml file that contains a template model hierarchy tree with a
         hierarchy node per color used in the input volume's color table. Color
         names used for the models are matched to template hierarchy names to
         create a multi level output tree. Create a hierarchy in the Models GUI
         and save a scene, then clean it up to remove everything but the model
         hierarchy and display nodes.

       --pad
         Pad the input volume with zero value voxels on all 6 faces in order to
         ensure the production of closed surfaces. Sets the origin translation
         and extent translation so that the models still line up with the
         unpadded input volume. (value: 0)

       --pointnormals
         Turn this flag on if you wish to calculate the normal vectors for the
         points. (value: 0)

       --splitnormals
         Splitting normals is useful for visualizing sharp features. However it
         creates holes in surfaces which affects measurements. (value: 0)

       --decimate <float>
         Chose the target reduction in number of polygons as a decimal
         percentage (between 0 and 1) of the number of polygons. Specifies the
         percentage of triangles to be removed. For example, 0.1 means 10%
         reduction and 0.9 means 90% reduction. (value: 0.25)

       --filtertype <Sinc|Laplacian>
         You can control the type of smoothing done on the models by selecting
         a filter type of either Sinc or Laplacian. (value: Sinc)

       --smooth <int>
         Here you can set the number of smoothing iterations for Laplacian
         smoothing, or the degree of the polynomial approximating the windowed
         Sinc function. Use 0 if you wish no smoothing. (value: 10)

       -j,  --jointsmooth
         This will ensure that all resulting models fit together smoothly, like
         jigsaw puzzle pieces. Otherwise the models will be smoothed
         independently and may overlap. (value: 0)

       --skipUnNamed
         Select this to not generate models from labels that do not have names
         defined in the color look up table associated with the input label
         map. If true, only models which have an entry in the color table will
         be generated.  If false, generate all models that exist within the
         label range. (value: 0)

       -e <int>,  --end <int>
         If you want to specify a continuous range of labels from which to
         generate models, enter the higher label here. Voxel value up to which
         to continue making models. Skip any values with zero voxels. (value:
         -1)

       -s <int>,  --start <int>
         If you want to specify a continuous range of labels from which to
         generate models, enter the lower label here. Voxel value from which to
         start making models. Used instead of the label list to specify a range
         (make sure the label list is empty or it will over ride this). (value:
         -1)

       -l <std::vector<int>>,  --labels <std::vector<int>>
         A comma separated list of label values from which to make models. f
         you specify a list of Labels, it will override any start/end label
         settings. If you click Generate All Models it will override the list
         of labels and any start/end label settings.

       --generateAll
         Generate models for all labels in the input volume. select this option
         if you want to create all models that correspond to all values in a
         labelmap volume (using the Joint Smoothing option below is useful with
         this option). Ignores Labels, Start Label, End Label settings. Skips
         label 0. (value: 0)

       -n <std::string>,  --name <std::string>
         Name to use for this model. Any text entered in the entry box will be
         the starting string for the created model file names. The label number
         and the color name will also be part of the file name. If making
         multiple models, use this as a prefix to the label and color name.
         (value: Model)

       --modelSceneFile <std::string>  (accepted multiple times)
         Generated models, under a model hierarchy node. Models are imported
         into Slicer under a model hierarchy node, and their colors are set by
         the color table associated with the input label map volume. The model
         hierarchy node must be created before running the model maker, by
         selecting Create New ModelHierarchy from the Models drop down menu. If
         you're running from the command line, a model hierarchy node in a new
         mrml scene will be created for you. (value: None)

       --color <std::string>
         Color table to make labels to colors and objects

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input label map. The Input Volume drop down menu is
         populated with the label map volumes that are present in the scene,
         select one from which to generate models.


       Description: Create 3D surface models from segmented data.<p>Models are
       imported into Slicer under a model hierarchy node in a MRML scene. The
       model colors are set by the color table associated with the input volume
       (these colours will only be visible if you load the model scene
       file).</p><p><b>IO:</b></p><p>Specify an <i>Input Volume</i> that is a
       segmented label map volume. Create a new <i>Models</i> hierarchy to
       provide a structure to contain the return models created from the input
       volume.</p><p><b>Create Multiple:</b></p><p>If you specify a list of
       <i>Labels</i>, it will over ride any start/end label settings.</p><p>If
       you click <i>Generate All</i> it will over ride the list of lables and
       any start/end label settings.</p><p><b>Model Maker
       Parameters:</b></p><p>You can set the number of smoothing iterations,
       target reduction in number of polygons (decimal percentage). Use 0 and 1
       if you wish no smoothing nor decimation.<br>You can set the flags to
       split normals or generate point normals in this pane as well.<br>You can
       save a copy of the models after intermediate steps (marching cubes,
       smoothing, and decimation if not joint smoothing, otherwise just after
       decimation); these models are not saved in the mrml file, turn off
       deleting temporary files first in the python
       window:<br><i>slicer.modules.modelmaker.cliModuleLogic().DeleteTemporary
       FilesOff()</i></p>

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH), Bill
       Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ModelToLabelMap

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ModelToLabelMap
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-l
                                            <int>] [--distance <float>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -l <int>,  --labelValue <int>
         The unsigned char label value to use in the output label map. (value:
         255)

       --distance <float>
         Determines how finely the surface is sampled. Used for the distance
         argument in the vtkPolyDataPointSampler. (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume

       <std::string>
         (required)  Input model

       <std::string>
         (required)  Unsigned char label map volume


       Description: Intersects an input model with an reference volume and
       produces an output label map. The algorithm uses flood fill from the
       model's center of mass, open models or ones with multiple pieces will
       not work well. The label map is constrained to be unsigned char, so the
       input label value is only valid in the range 0-255.

       Author(s): Nicole Aucoin (SPL, BWH), Xiaodong Tao (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### MultiplyScalarVolumes

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./MultiplyScalarVolumes
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--order <0|1|2|3>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --order <0|1|2|3>
         Interpolation order if two images are in different coordinate frames
         or have different sampling. (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume 1

       <std::string>
         (required)  Input volume 2

       <std::string>
         (required)  Volume1 * Volume2


       Description: Multiplies two images. Although all image types are
       supported on input, only signed types are produced. The two images do
       not have to have the same dimensions.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### N4ITKBiasFieldCorrection

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./N4ITKBiasFieldCorrection
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--nhistogrambins <int>]
                                            [--wienerfilternoise <float>]
                                            [--weightimage <std::string>]
                                            [--shrinkfactor <int>]
                                            [--bsplineorder <int>]
                                            [--convergencethreshold <float>]
                                            [--iterations <std::vector<int>>]
                                            [--bffwhm <float>]
                                            [--splinedistance <float>]
                                            [--meshresolution
                                            <std::vector<float>>]
                                            [--outputbiasfield <std::string>]
                                            [--maskimage <std::string>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --nhistogrambins <int>
         Number of histogram bins. Zero implies use of the default value.
         (value: 0)

       --wienerfilternoise <float>
         Wiener filter noise. Zero implies use of the default value. (value: 0)

       --weightimage <std::string>
         Weight Image

       --shrinkfactor <int>
         Defines how much the image should be upsampled before estimating the
         inhomogeneity field. Increase if you want to reduce the execution
         time. 1 corresponds to the original resolution. Larger values will
         significantly reduce the computation time. (value: 4)

       --bsplineorder <int>
         Order of B-spline used in the approximation. Larger values will lead
         to longer execution times, may result in overfitting and poor result.
         (value: 3)

       --convergencethreshold <float>
         Stopping criterion for the iterative bias estimation. Larger values
         will lead to smaller execution time. (value: 0.0001)

       --iterations <std::vector<int>>
         Maximum number of iterations at each level of resolution. Larger
         values will increase execution time, but may lead to better results.
         (value: 50,40,30)

       --bffwhm <float>
         Bias field Full Width at Half Maximum. Zero implies use of the default
         value. (value: 0)

       --splinedistance <float>
         An alternative means to define the spline grid, by setting the
         distance between the control points. This parameter is used only if
         the grid resolution is not specified. (value: 0)

       --meshresolution <std::vector<float>>
         Resolution of the initial bspline grid defined as a sequence of three
         numbers. The actual resolution will be defined by adding the bspline
         order (default is 3) to the resolution in each dimension specified
         here. For example, 1,1,1 will result in a 4x4x4 grid of control
         points. This parameter may need to be adjusted based on your input
         image. In the multi-resolution N4 framework, the resolution of the
         bspline grid at subsequent iterations will be doubled. The number of
         resolutions is implicitly defined by Number of iterations parameter
         (the size of this list is the number of resolutions) (value: 1,1,1)

       --outputbiasfield <std::string>
         Recovered bias field (OPTIONAL)

       --maskimage <std::string>
         Binary mask that defines the structure of your interest. NOTE: This
         parameter is OPTIONAL. If the mask is not specified, the module will
         use internally Otsu thresholding to define this mask. Better
         processing results can often be obtained when a meaningful mask is
         defined.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input image where you observe signal inhomegeneity

       <std::string>
         (required)  Result of processing


       Description: Performs image bias correction using N4 algorithm. This
       module is based on the ITK filters contributed in the following
       publication:  Tustison N, Gee J 'N4ITK: Nick's N3 ITK Implementation For
       MRI Bias Field Correction', The Insight Journal 2009 January-June,
       http://hdl.handle.net/10380/3053

       Author(s): Nick Tustison (UPenn), Andrey Fedorov (SPL, BWH), Ron Kikinis
       (SPL, BWH)

       Acknowledgements: The development of this module was partially supported
       by NIH grants R01 AA016748-01, R01 CA111288 and U01 CA151261 as well as
       by NA-MIC, NAC, NCIGT and the Slicer community.


### OrientScalarVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./OrientScalarVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-o
                                            <Axial|Coronal|Sagittal|RIP|LIP|RSP
                                            |LSP|RIA|LIA|RSA|LSA|IRP|ILP|SRP
                                            |SLP|IRA|ILA|SRA|SLA|RPI|LPI|RAI
                                            |LAI|RPS|LPS|RAS|LAS|PRI|PLI|ARI
                                            |ALI|PRS|PLS|ARS|ALS|IPR|SPR|IAR
                                            |SAR|IPL|SPL|IAL|SAL|PIR|PSR|AIR
                                            |ASR|PIL|PSL|AIL|ASL>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -o <Axial|Coronal|Sagittal|RIP|LIP|RSP|LSP|RIA|LIA|RSA|LSA|IRP|ILP|SRP
          |SLP|IRA|ILA|SRA|SLA|RPI|LPI|RAI|LAI|RPS|LPS|RAS|LAS|PRI|PLI|ARI|ALI
          |PRS|PLS|ARS|ALS|IPR|SPR|IAR|SAR|IPL|SPL|IAL|SAL|PIR|PSR|AIR|ASR|PIL
          |PSL|AIL|ASL>,  --orientation <Axial|Coronal|Sagittal|RIP|LIP|RSP|LSP
          |RIA|LIA|RSA|LSA|IRP|ILP|SRP|SLP|IRA|ILA|SRA|SLA|RPI|LPI|RAI|LAI|RPS
          |LPS|RAS|LAS|PRI|PLI|ARI|ALI|PRS|PLS|ARS|ALS|IPR|SPR|IAR|SAR|IPL|SPL
          |IAL|SAL|PIR|PSR|AIR|ASR|PIL|PSL|AIL|ASL>
         Orientation choices (value: LPS)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume 1

       <std::string>
         (required)  The oriented volume


       Description: Orients an output volume. Rearranges the slices in a volume
       according to the selected orientation. The slices are not interpolated.
       They are just reordered and/or permuted. The resulting volume will cover
       the original volume. NOTE: since Slicer takes into account the
       orientation of a volume, the re-oriented volume will not show any
       difference from the original volume, To see the difference, save the
       volume and display it with a system that either ignores the orientation
       of the image (e.g. Paraview) or displays individual images.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### OtsuThresholdImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./OtsuThresholdImageFilter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfBins <int>]
                                            [--outsideValue <int>]
                                            [--insideValue <int>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfBins <int>
         This is an advanced parameter. The number of bins in the histogram
         used to model the probability mass function of the two intensity
         distributions. Small numbers of bins may result in a more conservative
         threshold. The default should suffice for most applications.
         Experimentation is the only way to see the effect of varying this
         parameter. (value: 128)

       --outsideValue <int>
         The value assigned to pixels that are outside the computed threshold
         (value: 255)

       --insideValue <int>
         The value assigned to pixels that are inside the computed threshold
         (value: 0)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: This filter creates a binary thresholded image that
       separates an image into foreground and background components. The filter
       calculates the optimum threshold separating those two classes so that
       their combined spread (intra-class variance) is minimal (see
       http://en.wikipedia.org/wiki/Otsu%27s_method).  Then the filter applies
       that threshold to the input image using the
       itkBinaryThresholdImageFilter. The numberOfHistogram bins can be set for
       the Otsu Calculator. The insideValue and outsideValue can be set for the
       BinaryThresholdImageFilter.  The filter produces a labeled volume.



       The original reference is:



       N.Otsu, 'A threshold selection method from gray level histograms,' IEEE
       Trans.Syst.ManCybern.SMC-9,62-66 1979.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from Insight/Examples
       (copyright) Insight Software Consortium


### PETStandardUptakeValueComputation

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./PETStandardUptakeValueComputati
                                            on  [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-o
                                            <std::string>] [--color
                                            <std::string>] [-l <std::string>]
                                            [-v <std::string>] [-p
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -o <std::string>,  --csvFile <std::string>
         A table holding the output SUV values in comma separated lines, one
         per label. Optional.

       --color <std::string>
         Color table to to map labels to colors and names

       -l <std::string>,  --labelMap <std::string>
         Input label volume containing the volumes of interest

       -v <std::string>,  --petVolume <std::string>
         Input PET volume for SUVbw computation (must be the same volume as
         pointed to by the DICOM path!).

       -p <std::string>,  --petDICOMPath <std::string>
         Input path to a directory containing a PET volume containing DICOM
         header information for SUV computation

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Computes the standardized uptake value based on body
       weight. Takes an input PET image in DICOM and NRRD format (DICOM header
       must contain Radiopharmaceutical parameters). Produces a CSV file that
       contains patientID, studyDate, dose, labelID, suvmin, suvmax, suvmean,
       labelName for each volume of interest. It also displays some of the
       information as output strings in the GUI, the CSV file is optional in
       that case. The CSV file is appended to on each execution of the
       CLI.

       Author(s): Wendy Plesniak (SPL, BWH), Nicole Aucoin (SPL, BWH), Ron
       Kikinis (SPL, BWH)

       Acknowledgements: This work is funded by the Harvard Catalyst, and the
       National Alliance for Medical Image Computing (NAMIC), funded by the
       National Institutes of Health through the NIH Roadmap for Medical
       Research, Grant U54 EB005149.


### PerformMetricTest

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./PerformMetricTest
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfHistogramBins <int>]
                                            [--numberOfSamples <int>]
                                            [--metricType <MMI|MSE>]
                                            [--inputMovingImage <std::string>]
                                            [--inputFixedImage <std::string>]
                                            [--inputBSplineTransform
                                            <std::string>] [--] [--version]
                                            [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfHistogramBins <int>
         The number of historgram bins when MMI (Mattes) is metric type.
         (value: 50)

       --numberOfSamples <int>
         The number of voxels sampled for metric evaluation. (value: 0)

       --metricType <MMI|MSE>
         Comparison metric type (value: MMI)

       --inputMovingImage <std::string>


       --inputFixedImage <std::string>


       --inputBSplineTransform <std::string>
         Input transform that is use to warp moving image before metric
         comparison.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: Compare Mattes/MSQ metric value for two input images and a
       possible input BSpline transform.

       Author(s): Ali Ghayoor


### ProbeVolumeWithModel

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ProbeVolumeWithModel
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Volume to use to 'paint' the model

       <std::string>
         (required)  Input model

       <std::string>
         (required)  Output 'painted' model


       Description: Paint a model by a volume (using
       vtkProbeFilter).

       Author(s): Lauren O'Donnell (SPL, BWH)

       Acknowledgements: BWH, NCIGT/LMI


### ResampleDTIVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ResampleDTIVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-t <rt
                                            |a>] [-m <std::vector<double>>] [-o
                                            <int>] [-W <h|c|w|l|b>] [-p
                                            <double>] [-n <int>] [-d
                                            <std::vector<double>>] [-O
                                            <std::vector<float>>] [-z
                                            <std::vector<double>>] [-s
                                            <std::vector<double>>] [-b]
                                            [--image_center <input|output>]
                                            [-c] [-r <std::vector<float>>]
                                            [--spaceChange] [--notbulk]
                                            [--transform_order <input-to-output
                                            |output-to-input>] [-T <PPD|FS>]
                                            [--correction <zero|none|abs
                                            |nearest>] [--noMeasurementFrame]
                                            [-i <linear|nn|ws|bs>]
                                            [--hfieldtype <displacement
                                            |h-Field>] [-H <std::string>] [-f
                                            <std::string>] [-R <std::string>]
                                            [--] [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -t <rt|a>,  --transform <rt|a>
         Transform algorithm

         rt = Rigid Transform

         a = Affine Transform (value: a)

       -m <std::vector<double>>,  --transform_matrix <std::vector<double>>
         12 parameters of the transform matrix by rows ( --last 3 being
         translation-- ) (value: 1,0,0,0,1,0,0,0,1,0,0,0)

       -o <int>,  --spline_order <int>
         Spline Order (Spline order may be from 0 to 5) (value: 3)

       -W <h|c|w|l|b>,  --window_function <h|c|w|l|b>
         Window Function

         h = Hamming

         c = Cosine

         w = Welch

         l = Lanczos

         b = Blackman (value: c)

       -p <double>,  --default_pixel_value <double>
         Default pixel value for samples falling outside of the input region
         (value: 1e-10)

       -n <int>,  --number_of_thread <int>
         Number of thread used to compute the output image (value: 0)

       -d <std::vector<double>>,  --direction_matrix <std::vector<double>>
         9 parameters of the direction matrix by rows (ijk to LPS if LPS
         transform, ijk to RAS if RAS transform) (value: 0,0,0,0,0,0,0,0,0)

       -O <std::vector<float>>,  --origin <std::vector<float>>
         Origin of the output Image

       -z <std::vector<double>>,  --size <std::vector<double>>
         Size along each dimension (0 means use input size) (value: 0,0,0)

       -s <std::vector<double>>,  --spacing <std::vector<double>>
         Spacing along each dimension (0 means use input spacing) (value: 0,0
         ,0)

       -b,  --Inverse_ITK_Transformation
         Inverse the transformation before applying it from output image to
         input image (only for rigid and affine transforms) (value: 0)

       --image_center <input|output>
         Image to use to center the transform (used only if 'Centered
         Transform' is selected) (value: input)

       -c,  --centered_transform
         Set the center of the transformation to the center of the input image
         (only for rigid and affine transforms) (value: 0)

       -r <std::vector<float>>,  --rotation_point <std::vector<float>>
         Center of rotation (only for rigid and affine transforms) (value: 0,0
         ,0)

       --spaceChange
         Space Orientation between transform and image is different (RAS/LPS)
         (warning: if the transform is a Transform Node in Slicer3, do not
         select) (value: 0)

       --notbulk
         The transform following the BSpline transform is not set as a bulk
         transform for the BSpline transform (value: 0)

       --transform_order <input-to-output|output-to-input>
         Select in what order the transforms are read (value: output-to-input)

       -T <PPD|FS>,  --transform_tensor_method <PPD|FS>
         Chooses between 2 methods to transform the tensors: Finite Strain (FS)
         , faster but less accurate, or Preservation of the Principal Direction
         (PPD) (value: PPD)

       --correction <zero|none|abs|nearest>
         Correct the tensors if computed tensor is not semi-definite positive
         (value: zero)

       --noMeasurementFrame
         Do not use the measurement frame that is in the input image to
         transform the tensors. Uses the image orientation instead (value: 0)

       -i <linear|nn|ws|bs>,  --interpolation <linear|nn|ws|bs>
         Sampling algorithm (linear , nn (nearest neighborhoor), ws
         (WindowedSinc), bs (BSpline) ) (value: linear)

       --hfieldtype <displacement|h-Field>
         Set if the deformation field is an -Field (value: h-Field)

       -H <std::string>,  --defField <std::string>
         File containing the deformation field (3D vector image containing
         vectors with 3 components)

       -f <std::string>,  --transformationFile <std::string>


       -R <std::string>,  --Reference <std::string>
         Reference Volume (spacing,size,orientation,origin)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be resampled

       <std::string>
         (required)  Resampled Volume


       Description: Resampling an image is a very important task in image
       analysis. It is especially important in the frame of image registration.
       This module implements DT image resampling through the use of itk
       Transforms. The resampling is controlled by the Output Spacing.
       'Resampling' is performed in space coordinates, not pixel/grid
       coordinates. It is quite important to ensure that image spacing is
       properly set on the images involved. The interpolator is required since
       the mapping from one space to the other will often require evaluation of
       the intensity of the image at non-grid positions.

       Author(s): Francois Budin (UNC)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.
       Information on the National Centers for Biomedical Computing can be
       obtained from http://nihroadmap.nih.gov/bioinformatics


### ResampleScalarVectorDWIVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ResampleScalarVectorDWIVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-t <rt
                                            |a>] [-m <std::vector<double>>] [-o
                                            <int>] [-W <h|c|w|l|b>] [-p
                                            <double>] [-n <int>] [-d
                                            <std::vector<double>>] [-O
                                            <std::vector<float>>] [-z
                                            <std::vector<double>>] [-s
                                            <std::vector<double>>] [-b]
                                            [--image_center <input|output>]
                                            [-c] [-r <std::vector<float>>]
                                            [--spaceChange] [--notbulk]
                                            [--transform_order <input-to-output
                                            |output-to-input>] [-i <linear|nn
                                            |ws|bs>] [--hfieldtype
                                            <displacement|h-Field>] [-H
                                            <std::string>] [-f <std::string>]
                                            [-R <std::string>] [--] [--version]
                                            [-h] <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -t <rt|a>,  --transform <rt|a>
         Transform algorithm

         rt = Rigid Transform

         a = Affine Transform (value: a)

       -m <std::vector<double>>,  --transform_matrix <std::vector<double>>
         12 parameters of the transform matrix by rows ( --last 3 being
         translation-- ) (value: 1,0,0,0,1,0,0,0,1,0,0,0)

       -o <int>,  --spline_order <int>
         Spline Order (value: 3)

       -W <h|c|w|l|b>,  --window_function <h|c|w|l|b>
         Window Function

         h = Hamming

         c = Cosine

         w = Welch

         l = Lanczos

         b = Blackman (value: c)

       -p <double>,  --default_pixel_value <double>
         Default pixel value for samples falling outside of the input region
         (value: 0)

       -n <int>,  --number_of_thread <int>
         Number of thread used to compute the output image (value: 0)

       -d <std::vector<double>>,  --direction_matrix <std::vector<double>>
         9 parameters of the direction matrix by rows (ijk to LPS if LPS
         transform, ijk to RAS if RAS transform) (value: 0,0,0,0,0,0,0,0,0)

       -O <std::vector<float>>,  --origin <std::vector<float>>
         Origin of the output Image

       -z <std::vector<double>>,  --size <std::vector<double>>
         Size along each dimension (0 means use input size) (value: 0,0,0)

       -s <std::vector<double>>,  --spacing <std::vector<double>>
         Spacing along each dimension (0 means use input spacing) (value: 0,0
         ,0)

       -b,  --Inverse_ITK_Transformation
         Inverse the transformation before applying it from output image to
         input image (value: 0)

       --image_center <input|output>
         Image to use to center the transform (used only if 'Centered
         Transform' is selected) (value: input)

       -c,  --centered_transform
         Set the center of the transformation to the center of the input image
         (value: 0)

       -r <std::vector<float>>,  --rotation_point <std::vector<float>>
         Rotation Point in case of rotation around a point (otherwise useless)
         (value: 0,0,0)

       --spaceChange
         Space Orientation between transform and image is different (RAS/LPS)
         (warning: if the transform is a Transform Node in Slicer3, do not
         select) (value: 0)

       --notbulk
         The transform following the BSpline transform is not set as a bulk
         transform for the BSpline transform (value: 0)

       --transform_order <input-to-output|output-to-input>
         Select in what order the transforms are read (value: output-to-input)

       -i <linear|nn|ws|bs>,  --interpolation <linear|nn|ws|bs>
         Sampling algorithm (linear or nn (nearest neighborhoor), ws
         (WindowedSinc), bs (BSpline) ) (value: linear)

       --hfieldtype <displacement|h-Field>
         Set if the deformation field is an h-Field (value: h-Field)

       -H <std::string>,  --defField <std::string>
         File containing the deformation field (3D vector image containing
         vectors with 3 components)

       -f <std::string>,  --transformationFile <std::string>


       -R <std::string>,  --Reference <std::string>
         Reference Volume (spacing,size,orientation,origin)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input Volume to be resampled

       <std::string>
         (required)  Resampled Volume


       Description: This module implements image and vector-image resampling
       through  the use of itk Transforms.It can also handle diffusion weighted
       MRI image resampling. 'Resampling' is performed in space coordinates,
       not pixel/grid coordinates. It is quite important to ensure that image
       spacing is properly set on the images involved. The interpolator is
       required since the mapping from one space to the other will often
       require evaluation of the intensity of the image at non-grid positions.




       Warning: To resample DWMR Images, use nrrd input and output files.




       Warning: Do not use to resample Diffusion Tensor Images, tensors would
       not be reoriented

       Author(s): Francois Budin (UNC)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.
       Information on the National Centers for Biomedical Computing can be
       obtained from http://nihroadmap.nih.gov/bioinformatics


### ResampleScalarVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ResampleScalarVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-i
                                            <linear|nearestNeighbor|bspline
                                            |hamming|cosine|welch|lanczos
                                            |blackman>] [-s
                                            <std::vector<float>>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -i <linear|nearestNeighbor|bspline|hamming|cosine|welch|lanczos
          |blackman>,  --interpolation <linear|nearestNeighbor|bspline|hamming
          |cosine|welch|lanczos|blackman>
         Sampling algorithm (linear, nearest neighbor, bspline(cubic)  or
         windowed sinc). There are several sinc algorithms available as
         described in the following publication: Erik H. W. Meijering, Wiro J.
         Niessen, Josien P. W. Pluim, Max A. Viergever: Quantitative Comparison
         of Sinc-Approximating Kernels for Medical Image Interpolation. MICCAI
         1999, pp. 210-217. Each window has a radius of 3; (value: linear)

       -s <std::vector<float>>,  --spacing <std::vector<float>>
         Spacing along each dimension (0 means use input spacing) (value: 0,0
         ,0)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be resampled

       <std::string>
         (required)  Resampled Volume


       Description: Resampling an image is an important task in image analysis.
       It is especially important in the frame of image registration. This
       module implements image resampling through the use of itk Transforms.
       This module uses an Identity Transform. The resampling is controlled by
       the Output Spacing. 'Resampling' is performed in space coordinates, not
       pixel/grid coordinates. It is quite important to ensure that image
       spacing is properly set on the images involved. The interpolator is
       required since the mapping from one space to the other will often
       require evaluation of the intensity of the image at non-grid positions.
       Several interpolators are available: linear, nearest neighbor, bspline
       and five flavors of sinc. The sinc interpolators, although more precise,
       are much slower than the linear and nearest neighbor interpolator. To
       resample label volumnes, nearest neighbor interpolation should be used
       exclusively.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### RobustStatisticsSegmenter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./RobustStatisticsSegmenter
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--maxRunningTime <double>]
                                            [--labelValue <int>] [-c <double>]
                                            [--intensityHomogeneity <double>]
                                            [-v <double>] [--] [--version] [-h]
                                            <std::string> <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --maxRunningTime <double>
         The program will stop if this time is reached. (value: 10)

       --labelValue <int>
         Label value of the output image (value: 1)

       -c <double>,  --curvatureWeight <double>
         Given sphere 1.0 score and extreme rough bounday/surface 0 score, what
         is the expected smoothness of the object? (value: 0.5)

       --intensityHomogeneity <double>
         What is the homogeneity of intensity within the object? Given constant
         intensity at 1.0 score and extreme fluctuating intensity at 0. (value:
         0.6)

       -v <double>,  --expectedVolume <double>
         The approximate volume of the object, in mL. (value: 50)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Original image to be segmented

       <std::string>
         (required)  Label image for initialization

       <std::string>
         (required)  Segmented image


       Description: Active contour segmentation using robust
       statistic.

       Author(s): Yi Gao (gatech), Allen Tannenbaum (gatech), Ron Kikinis (SPL,
       BWH)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health


### SimpleRegionGrowingSegmentation

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./SimpleRegionGrowingSegmentation
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [--seed
                                            <std::vector<std::vector<float> >>]
                                            ...  [--labelvalue <int>]
                                            [--neighborhood <int>]
                                            [--multiplier <double>]
                                            [--iterations <int>] [--timestep
                                            <double>] [--smoothingIterations
                                            <int>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --seed <std::vector<std::vector<float> >>  (accepted multiple times)
         Seed point(s) for region growing (value: None)

       --labelvalue <int>
         The integer value (0-255) to use for the segmentation results. This
         will determine the color of the segmentation that will be generated by
         the Region growing algorithm (value: 2)

       --neighborhood <int>
         The radius of the neighborhood over which to calculate intensity model
         (value: 1)

       --multiplier <double>
         Number of standard deviations to include in intensity model (value:
         2.5)

       --iterations <int>
         Number of iterations of region growing (value: 5)

       --timestep <double>
         Timestep for curvature flow (value: 0.0625)

       --smoothingIterations <int>
         Number of smoothing iterations (value: 5)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: A simple region growing segmentation algorithm based on
       intensity statistics. To create a list of fiducials (Seeds) for this
       algorithm, click on the tool bar icon of an arrow pointing to a sphere
       fiducial to enter the 'place a new object mode' and then use the Markups
       module. This module uses the Slicer Command Line Interface (CLI) and the
       ITK filters CurvatureFlowImageFilter and
       ConfidenceConnectedImageFilter.

       Author(s): Jim Miller (GE)

       Acknowledgements: This command module was derived from Insight/Examples
       (copyright) Insight Software Consortium


### SubtractScalarVolumes

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./SubtractScalarVolumes
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--order <0|1|2|3>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --order <0|1|2|3>
         Interpolation order if two images are in different coordinate frames
         or have different sampling. (value: 1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume 1

       <std::string>
         (required)  Input volume 2

       <std::string>
         (required)  Volume1 - Volume2


       Description: Subtracts two images. Although all image types are
       supported on input, only signed types are produced. The two images do
       not have to have the same dimensions.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### ThresholdScalarVolume

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./ThresholdScalarVolume
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>] [-n]
                                            [-v <float>] [-u <float>] [-l
                                            <float>] [-t <float>]
                                            [--thresholdtype <Below|Above
                                            |Outside>] [--] [--version] [-h]
                                            <std::string> <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       -n,  --negate
         Swap the outside value with the inside value. (value: 0)

       -v <float>,  --outsidevalue <float>
         Set the voxels to this value if they fall outside the threshold range
         (value: 0)

       -u <float>,  --upper <float>
         Upper threshold value (value: 200)

       -l <float>,  --lower <float>
         Lower threshold value (value: 1)

       -t <float>,  --threshold <float>
         Threshold value (value: 128)

       --thresholdtype <Below|Above|Outside>
         What kind of threshold to perform. If Outside is selected, uses Upper
         and Lower values. If Below is selected, uses the ThresholdValue, if
         Above is selected, uses the ThresholdValue. (value: Outside)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume

       <std::string>
         (required)  Thresholded input volume


       Description: <p>Threshold an image.</p><p>Set image values to a
       user-specified outside value if they are below, above, or between simple
       threshold values.</p><p>ThresholdAbove: The values greater than or equal
       to the threshold value are set to OutsideValue.</p><p>ThresholdBelow:
       The values less than or equal to the threshold value are set to
       OutsideValue.</p><p>ThresholdOutside: The values outside the range
       Lower-Upper are set to OutsideValue.</p>

       Author(s): Nicole Aucoin (SPL, BWH), Ron Kikinis (SPL, BWH), Julien
       Finet (Kitware)

       Acknowledgements: This work is part of the National Alliance for Medical
       Image Computing (NAMIC), funded by the National Institutes of Health
       through the NIH Roadmap for Medical Research, Grant U54 EB005149.


### VBRAINSDemonWarp

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./VBRAINSDemonWarp
                                            [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--numberOfThreads <int>]
                                            [--numberOfBCHApproximationTerms
                                            <int>] [-p] [-G] [-a] [-l <double>]
                                            [-g <double>] [-t <0|1|2>] [-w
                                            <std::vector<float>>] [-v]
                                            [--outputNormalized]
                                            [--checkerboardPatternSubdivisions
                                            <std::vector<int>>]
                                            [--outputCheckerboardVolume
                                            <std::string>]
                                            [--outputDisplacementFieldPrefix
                                            <std::string>]
                                            [--neighborhoodForBOBF
                                            <std::vector<int>>] [--seedForBOBF
                                            <std::vector<int>>]
                                            [--backgroundFillValue <int>]
                                            [--upperThresholdForBOBF <int>]
                                            [--lowerThresholdForBOBF <int>]
                                            [--movingBinaryVolume
                                            <std::string>] [--fixedBinaryVolume
                                            <std::string>] [--makeBOBF]
                                            [--initializeWithTransform
                                            <std::string>]
                                            [--initializeWithDisplacementField
                                            <std::string>] [--medianFilterSize
                                            <std::vector<int>>]
                                            [--numberOfMatchPoints <int>]
                                            [--numberOfHistogramBins <int>]
                                            [-e] [-i <std::vector<int>>]
                                            [--minimumMovingPyramid
                                            <std::vector<int>>]
                                            [--minimumFixedPyramid
                                            <std::vector<int>>] [-n <int>] [-s
                                            <double>] [--registrationFilterType
                                            <Demons|FastSymmetricForces
                                            |Diffeomorphic|LogDemons
                                            |SymmetricLogDemons>]
                                            [--interpolationMode
                                            <NearestNeighbor|Linear
                                            |ResampleInPlace|BSpline
                                            |WindowedSinc|Hamming|Cosine|Welch
                                            |Lanczos|Blackman>]
                                            [--outputPixelType <float|short
                                            |ushort|int|uchar>] [-O
                                            <std::string>] [-o <std::string>]
                                            [--inputPixelType <float|short
                                            |ushort|int|uchar>] [-f
                                            <std::vector<std::string>>] ...
                                            [-m <std::vector<std::string>>] ...
                                            [--] [--version] [-h]


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --numberOfThreads <int>
         Explicitly specify the maximum number of threads to use. (value: -1)

       --numberOfBCHApproximationTerms <int>
         Number of terms in the BCH expansion (value: 2)

       -p,  --promptUser
         Prompt the user to hit enter each time an image is sent to the
         DebugImageViewer (value: 0)

       -G,  --gui
         Display intermediate image volumes for debugging (value: 0)

       -a,  --use_vanilla_dem
         Run vanilla demons algorithm (value: 0)

       -l <double>,  --max_step_length <double>
         Maximum length of an update vector (0: no restriction) (value: 2)

       -g <double>,  --upFieldSmoothing <double>
         Smoothing sigma for the update field at each iteration (value: 0)

       -t <0|1|2>,  --gradient_type <0|1|2>
         Type of gradient used for computing the demons force (0 is symmetrized
         , 1 is fixed image, 2 is moving image) (value: 0)

       -w <std::vector<float>>,  --weightFactors <std::vector<float>>
         Weight fatctors for each input images (value: 0.5,0.5)

       -v,  --outputDebug
         Flag to write debugging images after each step. (value: 0)

       --outputNormalized
         Flag to warp and write the normalized images to output.  In normalized
         images the image values are fit-scaled to be between 0 and the maximum
         storage type value. (value: 0)

       --checkerboardPatternSubdivisions <std::vector<int>>
         Number of Checkerboard subdivisions in all 3 directions (value: 4,4,4)

       --outputCheckerboardVolume <std::string>
         Genete a checkerboard image volume between the fixedVolume and the
         deformed movingVolume.

       --outputDisplacementFieldPrefix <std::string>
         Displacement field filename prefix for writing separate x, y, and z
         component images (value: none)

       --neighborhoodForBOBF <std::vector<int>>
         neighborhood in all 3 directions to be included when performing BOBF
         (value: 1,1,1)

       --seedForBOBF <std::vector<int>>
         coordinates in all 3 directions for Seed when performing BOBF (value:
         0,0,0)

       --backgroundFillValue <int>
         Replacement value to overwrite background when performing BOBF (value:
         0)

       --upperThresholdForBOBF <int>
         Upper threshold for performing BOBF (value: 70)

       --lowerThresholdForBOBF <int>
         Lower threshold for performing BOBF (value: 0)

       --movingBinaryVolume <std::string>
         Mask filename for desired region of interest in the Moving image.

       --fixedBinaryVolume <std::string>
         Mask filename for desired region of interest in the Fixed image.

       --makeBOBF
         Flag to make Brain-Only Background-Filled versions of the input and
         target volumes. (value: 0)

       --initializeWithTransform <std::string>
         Initial Transform filename

       --initializeWithDisplacementField <std::string>
         Initial deformation field vector image file name

       --medianFilterSize <std::vector<int>>
         Median filter radius in all 3 directions.  When images have a lot of
         salt and pepper noise, this step can improve the registration. (value:
         0,0,0)

       --numberOfMatchPoints <int>
         The number of match points for histrogramMatch (value: 2)

       --numberOfHistogramBins <int>
         The number of histogram levels (value: 256)

       -e,  --histogramMatch
         Histogram Match the input images.  This is suitable for images of the
         same modality that may have different absolute scales, but the same
         overall intensity profile. (value: 0)

       -i <std::vector<int>>,  --arrayOfPyramidLevelIterations
          <std::vector<int>>
         The number of iterations for each pyramid level (value: 100,100,100)

       --minimumMovingPyramid <std::vector<int>>
         The shrink factor for the first level of the moving image pyramid.
         (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally
         full scale) (value: 16,16,16)

       --minimumFixedPyramid <std::vector<int>>
         The shrink factor for the first level of the fixed image pyramid.
         (i.e. start at 1/16 scale, then 1/8, then 1/4, then 1/2, and finally
         full scale) (value: 16,16,16)

       -n <int>,  --numberOfPyramidLevels <int>
         Number of image pyramid levels to use in the multi-resolution
         registration. (value: 5)

       -s <double>,  --smoothDisplacementFieldSigma <double>
         A gaussian smoothing value to be applied to the deformation feild at
         each iteration. (value: 1)

       --registrationFilterType <Demons|FastSymmetricForces|Diffeomorphic
          |LogDemons|SymmetricLogDemons>
         Registration Filter Type: Demons|FastSymmetricForces|Diffeomorphic
         |LogDemons|SymmetricLogDemons (value: Diffeomorphic)

       --interpolationMode <NearestNeighbor|Linear|ResampleInPlace|BSpline
          |WindowedSinc|Hamming|Cosine|Welch|Lanczos|Blackman>
         Type of interpolation to be used when applying transform to moving
         volume.  Options are Linear, ResampleInPlace, NearestNeighbor, BSpline
         , or WindowedSinc (value: Linear)

       --outputPixelType <float|short|ushort|int|uchar>
         outputVolume will be typecast to this format: float|short|ushort|int
         |uchar (value: float)

       -O <std::string>,  --outputDisplacementFieldVolume <std::string>
         Output deformation field vector image (will have the same physical
         space as the fixedVolume).

       -o <std::string>,  --outputVolume <std::string>
         Required: output resampled moving image (will have the same physical
         space as the fixedVolume).

       --inputPixelType <float|short|ushort|int|uchar>
         Input volumes will be typecast to this format: float|short|ushort|int
         |uchar (value: float)

       -f <std::vector<std::string>>,  --fixedVolume <std::vector<std::string>>
          (accepted multiple times)
         Required: input fixed (target) image

       -m <std::vector<std::string>>,  --movingVolume
          <std::vector<std::string>>  (accepted multiple times)
         Required: input moving image

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.


       Description: This program finds a deformation field to warp a moving
       image onto a fixed image.  The images must be of the same signal kind,
       and contain an image of the same kind of object.  This program uses the
       Thirion Demons warp software in ITK, the Insight Toolkit.  Additional
       information is available at:
       http://www.nitrc.org/projects/brainsdemonwarp.

       Author(s): This tool was developed by Hans J. Johnson and Greg
       Harris.

       Acknowledgements: The development of this tool was supported by funding
       from grants NS050568 and NS40068 from the National Institute of
       Neurological Disorders and Stroke and grants MH31593, MH40856, from the
       National Institute of Mental Health.


### VotingBinaryHoleFillingImageFilter

    Usage
      Slicer [options]

    Options
      --launcher-help                              Display help
      --launcher-version                           Show launcher version information
      --launcher-verbose                           Verbose mode
      --launch                                     Specify the application to launch
      --launcher-detach                            Launcher will NOT wait for the application to finish
      --launcher-no-splash                         Hide launcher splash
      --launcher-timeout                           Specify the time in second before the launcher kills the application. -1 means no timeout (default: -1)
      --launcher-load-environment                  Specify the saved environment to load.
      --launcher-dump-environment                  Launcher will print environment variables to be set, then exit
      --launcher-show-set-environment-commands     Launcher will print commands suitable for setting the parent environment (i.e. using 'eval' in a POSIX shell), then exit
      --launcher-additional-settings               Additional settings file to consider
      --launcher-ignore-user-additional-settings   Ignore additional user settings
      --launcher-generate-exec-wrapper-script      Generate executable wrapper script allowing to set the environment
      --launcher-generate-template                 Generate an example of setting file

    USAGE:

       /opt/slicer/lib/Slicer-4.8/cli-modules/./VotingBinaryHoleFillingImageFil
                                            ter  [--returnparameterfile
                                            <std::string>]
                                            [--processinformationaddress
                                            <std::string>] [--xml] [--echo]
                                            [--deserialize <std::string>]
                                            [--serialize <std::string>]
                                            [--foreground <int>] [--background
                                            <int>] [--majorityThreshold <int>]
                                            [--radius <std::vector<int>>] [--]
                                            [--version] [-h] <std::string>
                                            <std::string>


    Where:

       --returnparameterfile <std::string>
         Filename in which to write simple return parameters (int, float,
         int-vector, etc.) as opposed to bulk return parameters (image,
         geometry, transform, measurement, table).

       --processinformationaddress <std::string>
         Address of a structure to store process information (progress, abort,
         etc.). (value: 0)

       --xml
         Produce xml description of command line arguments (value: 0)

       --echo
         Echo the command line arguments (value: 0)

       --deserialize <std::string>
         Restore the module's parameters that were previously archived.

       --serialize <std::string>
         Store the module's parameters to a file.

       --foreground <int>
         The value associated with the foreground (object) (value: 255)

       --background <int>
         The value associated with the background (not object) (value: 0)

       --majorityThreshold <int>
         The number of pixels over 50% that will decide whether an OFF pixel
         will become ON or not. For example, if the neighborhood of a pixel has
         124 pixels (excluding itself), the 50% will be 62, and if you set a
         Majority threshold of 5, that means that the filter will require 67 or
         more neighbor pixels to be ON in order to switch the current OFF pixel
         to ON. (value: 1)

       --radius <std::vector<int>>
         The radius of a hole to be filled (value: 1,1,1)

       --,  --ignore_rest
         Ignores the rest of the labeled arguments following this flag.

       --version
         Displays version information and exits.

       -h,  --help
         Displays usage information and exits.

       <std::string>
         (required)  Input volume to be filtered

       <std::string>
         (required)  Output filtered


       Description: Applies a voting operation in order to fill-in cavities.
       This can be used for smoothing contours and for filling holes in binary
       images. This technique is used frequently when segmenting complete
       organs that may have ducts or vasculature that may not have been
       included in the initial segmentation, e.g. lungs, kidneys,
       liver.

       Author(s): Bill Lorensen (GE)

       Acknowledgements: This command module was derived from
       Insight/Examples/Filtering/VotingBinaryHoleFillingImageFilter
       (copyright) Insight Software Consortium
