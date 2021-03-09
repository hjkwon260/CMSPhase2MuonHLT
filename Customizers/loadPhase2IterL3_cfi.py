import FWCore.ParameterSet.Config as cms

def loadPhase2IterL3(process, processName = "MYHLT"):

    ################################
    ### HLT Reconstruction sequences
    ################################

    process.hltTriggerType = cms.EDFilter("HLTTriggerTypeFilter",
        SelectedTriggerType = cms.int32(1)
    )

    # process.hltGtStage2Digis = cms.EDProducer("L1TRawToDigi",
    #     CTP7 = cms.untracked.bool(False),
    #     FWId = cms.uint32(0),
    #     FWOverride = cms.bool(False),
    #     FedIds = cms.vint32(1404),
    #     InputLabel = cms.InputTag("rawDataCollector"),
    #     MTF7 = cms.untracked.bool(False),
    #     MinFeds = cms.uint32(0),
    #     Setup = cms.string('stage2::GTSetup'),
    #     TMTCheck = cms.bool(True),
    #     debug = cms.untracked.bool(False),
    #     lenAMC13Header = cms.untracked.int32(8),
    #     lenAMC13Trailer = cms.untracked.int32(8),
    #     lenAMCHeader = cms.untracked.int32(8),
    #     lenAMCTrailer = cms.untracked.int32(0),
    #     lenSlinkHeader = cms.untracked.int32(8),
    #     lenSlinkTrailer = cms.untracked.int32(8)
    # )


    # process.hltGtStage2ObjectMap = cms.EDProducer("L1TGlobalProducer",
    #     AlgoBlkInputTag = cms.InputTag("hltGtStage2Digis"),
    #     AlgorithmTriggersUnmasked = cms.bool(True),
    #     AlgorithmTriggersUnprescaled = cms.bool(True),
    #     AlternativeNrBxBoardDaq = cms.uint32(0),
    #     BstLengthBytes = cms.int32(-1),
    #     EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    #     EmulateBxInEvent = cms.int32(1),
    #     EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    #     ExtInputTag = cms.InputTag("hltGtStage2Digis"),
    #     GetPrescaleColumnFromData = cms.bool(False),
    #     JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    #     L1DataBxInEvent = cms.int32(5),
    #     MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    #     PrescaleCSVFile = cms.string('prescale_L1TGlobal.csv'),
    #     PrescaleSet = cms.uint32(1),
    #     PrintL1Menu = cms.untracked.bool(False),
    #     ProduceL1GtDaqRecord = cms.bool(True),
    #     ProduceL1GtObjectMapRecord = cms.bool(True),
    #     TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    #     TriggerMenuLuminosity = cms.string('startup'),
    #     Verbosity = cms.untracked.int32(0)
    # )

    process.hltScalersRawToDigi = cms.EDProducer("ScalersRawToDigi",
        scalersInputTag = cms.InputTag("rawDataCollector")
    )

    process.hltOnlineBeamSpot = cms.EDProducer("BeamSpotOnlineProducer",
        changeToCMSCoordinates = cms.bool(False),
        gtEvmLabel = cms.InputTag(""),
        maxRadius = cms.double(2.0),
        maxZ = cms.double(40.0),
        setSigmaZ = cms.double(0.0),
        src = cms.InputTag("hltScalersRawToDigi")
    )

    # process.HLTL1UnpackerSequence = cms.Sequence(process.hltGtStage2Digis+process.hltGtStage2ObjectMap)
    process.HLTBeamSpot = cms.Sequence(process.hltScalersRawToDigi+process.hltOnlineBeamSpot)

    ### with L1 emulation
    # process.HLTBeginSequence = cms.Sequence(process.hltTriggerType+process.HLTL1UnpackerSequence+process.HLTBeamSpot)
    process.HLTBeginSequence = cms.Sequence(process.hltTriggerType+process.HLTBeamSpot)

    ### without L1 emulation 
    #process.HLTBeginSequence = cms.Sequence(process.hltTriggerType+process.HLTBeamSpot)


    ################################################################################################
    ### L2 Muon reconstruction sequences (local reco + global patter recognition in the muon system)
    ################################################################################################

    ## DT Phase1 unpacker not used 
    process.hltMuonDTDigis = cms.EDProducer("DTuROSRawToDigi",
        debug = cms.untracked.bool(False),
        inputLabel = cms.InputTag("rawDataCollector")
    )

    ## replacing the digis with simDigis
    process.hltDt1DRecHits = cms.EDProducer("DTRecHitProducer",
        debug = cms.untracked.bool(False),
        dtDigiLabel = cms.InputTag("simMuonDTDigis"),
        recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
        recAlgoConfig = cms.PSet(
            debug = cms.untracked.bool(False),
            doVdriftCorr = cms.bool(True),
            maxTime = cms.double(420.0),
            minTime = cms.double(-3.0),
            stepTwoFromDigi = cms.bool(False),
            tTrigMode = cms.string('DTTTrigSyncFromDB'),
            tTrigModeConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                doT0Correction = cms.bool(True),
                doTOFCorrection = cms.bool(True),
                doWirePropCorrection = cms.bool(True),
                tTrigLabel = cms.string(''),
                tofCorrType = cms.int32(0),
                vPropWire = cms.double(24.4),
                wirePropCorrType = cms.int32(0)
            ),
            useUncertDB = cms.bool(True)
        )
    )


    process.hltDt4DSegments = cms.EDProducer("DTRecSegment4DProducer",
        Reco4DAlgoConfig = cms.PSet(
            AllDTRecHits = cms.bool(True),
            Reco2DAlgoConfig = cms.PSet(
                AlphaMaxPhi = cms.double(1.0),
                AlphaMaxTheta = cms.double(0.9),
                MaxAllowedHits = cms.uint32(50),
                debug = cms.untracked.bool(False),
                hit_afterT0_resolution = cms.double(0.03),
                nSharedHitsMax = cms.int32(2),
                nUnSharedHitsMin = cms.int32(2),
                performT0SegCorrection = cms.bool(False),
                performT0_vdriftSegCorrection = cms.bool(False),
                perform_delta_rejecting = cms.bool(False),
                recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
                recAlgoConfig = cms.PSet(
                    debug = cms.untracked.bool(False),
                    doVdriftCorr = cms.bool(True),
                    maxTime = cms.double(420.0),
                    minTime = cms.double(-3.0),
                    stepTwoFromDigi = cms.bool(False),
                    tTrigMode = cms.string('DTTTrigSyncFromDB'),
                    tTrigModeConfig = cms.PSet(
                        debug = cms.untracked.bool(False),
                        doT0Correction = cms.bool(True),
                        doTOFCorrection = cms.bool(True),
                        doWirePropCorrection = cms.bool(True),
                        tTrigLabel = cms.string(''),
                        tofCorrType = cms.int32(0),
                        vPropWire = cms.double(24.4),
                        wirePropCorrType = cms.int32(0)
                    ),
                    useUncertDB = cms.bool(True)
                ),
                segmCleanerMode = cms.int32(2)
            ),
            Reco2DAlgoName = cms.string('DTCombinatorialPatternReco'),
            debug = cms.untracked.bool(False),
            hit_afterT0_resolution = cms.double(0.03),
            nSharedHitsMax = cms.int32(2),
            nUnSharedHitsMin = cms.int32(2),
            performT0SegCorrection = cms.bool(False),
            performT0_vdriftSegCorrection = cms.bool(False),
            perform_delta_rejecting = cms.bool(False),
            recAlgo = cms.string('DTLinearDriftFromDBAlgo'),
            recAlgoConfig = cms.PSet(
                debug = cms.untracked.bool(False),
                doVdriftCorr = cms.bool(True),
                maxTime = cms.double(420.0),
                minTime = cms.double(-3.0),
                stepTwoFromDigi = cms.bool(False),
                tTrigMode = cms.string('DTTTrigSyncFromDB'),
                tTrigModeConfig = cms.PSet(
                    debug = cms.untracked.bool(False),
                    doT0Correction = cms.bool(True),
                    doTOFCorrection = cms.bool(True),
                    doWirePropCorrection = cms.bool(True),
                    tTrigLabel = cms.string(''),
                    tofCorrType = cms.int32(0),
                    vPropWire = cms.double(24.4),
                    wirePropCorrType = cms.int32(0)
                ),
                useUncertDB = cms.bool(True)
            ),
            segmCleanerMode = cms.int32(2)
        ),
        Reco4DAlgoName = cms.string('DTCombinatorialPatternReco4D'),
        debug = cms.untracked.bool(False),
        recHits1DLabel = cms.InputTag("hltDt1DRecHits"),
        recHits2DLabel = cms.InputTag("dt2DSegments")
    )

    ## CSC Phase1 unpacker not used 
    process.hltMuonCSCDigis = cms.EDProducer("CSCDCCUnpacker",
        Debug = cms.untracked.bool(False),
        ErrorMask = cms.uint32(0),
        ExaminerMask = cms.uint32(535558134),
        FormatedEventDump = cms.untracked.bool(False),
        InputObjects = cms.InputTag("rawDataCollector"),
        PrintEventNumber = cms.untracked.bool(False),
        SuppressZeroLCT = cms.untracked.bool(True),
        UnpackStatusDigis = cms.bool(False),
        UseExaminer = cms.bool(True),
        UseFormatStatus = cms.bool(True),
        UseSelectiveUnpacking = cms.bool(True),
        VisualFEDInspect = cms.untracked.bool(False),
        VisualFEDShort = cms.untracked.bool(False),
        runDQM = cms.untracked.bool(False)
    )

    ## replacing upacked digis with simDigis
    ## stripDigiTag = cms.InputTag("hltMuonCSCDigis","MuonCSCStripDigi"),
    ## wireDigiTag = cms.InputTag("hltMuonCSCDigis","MuonCSCWireDigi")
    process.hltCsc2DRecHits = cms.EDProducer("CSCRecHitDProducer",
        CSCDebug = cms.untracked.bool(False),
        CSCNoOfTimeBinsForDynamicPedestal = cms.int32(2),
        CSCStripClusterChargeCut = cms.double(25.0),
        CSCStripClusterSize = cms.untracked.int32(3),
        CSCStripPeakThreshold = cms.double(10.0),
        CSCStripxtalksOffset = cms.double(0.03),
        CSCUseCalibrations = cms.bool(True),
        CSCUseGasGainCorrections = cms.bool(False),
        CSCUseReducedWireTimeWindow = cms.bool(False),
        CSCUseStaticPedestals = cms.bool(False),
        CSCUseTimingCorrections = cms.bool(True),
        CSCWireClusterDeltaT = cms.int32(1),
        CSCWireTimeWindowHigh = cms.int32(15),
        CSCWireTimeWindowLow = cms.int32(0),
        CSCstripWireDeltaTime = cms.int32(8),
        ConstSyst_ME12 = cms.double(0.02),
        ConstSyst_ME13 = cms.double(0.03),
        ConstSyst_ME1a = cms.double(0.01),
        ConstSyst_ME1b = cms.double(0.02),
        ConstSyst_ME21 = cms.double(0.03),
        ConstSyst_ME22 = cms.double(0.03),
        ConstSyst_ME31 = cms.double(0.03),
        ConstSyst_ME32 = cms.double(0.03),
        ConstSyst_ME41 = cms.double(0.03),
        NoiseLevel_ME12 = cms.double(7.0),
        NoiseLevel_ME13 = cms.double(4.0),
        NoiseLevel_ME1a = cms.double(9.0),
        NoiseLevel_ME1b = cms.double(6.0),
        NoiseLevel_ME21 = cms.double(5.0),
        NoiseLevel_ME22 = cms.double(7.0),
        NoiseLevel_ME31 = cms.double(5.0),
        NoiseLevel_ME32 = cms.double(7.0),
        NoiseLevel_ME41 = cms.double(5.0),
        UseAverageTime = cms.bool(False),
        UseFivePoleFit = cms.bool(True),
        UseParabolaFit = cms.bool(False),
        XTasymmetry_ME12 = cms.double(0.015),
        XTasymmetry_ME13 = cms.double(0.02),
        XTasymmetry_ME1a = cms.double(0.023),
        XTasymmetry_ME1b = cms.double(0.01),
        XTasymmetry_ME21 = cms.double(0.023),
        XTasymmetry_ME22 = cms.double(0.023),
        XTasymmetry_ME31 = cms.double(0.023),
        XTasymmetry_ME32 = cms.double(0.023),
        XTasymmetry_ME41 = cms.double(0.023),
        readBadChambers = cms.bool(True),
        readBadChannels = cms.bool(False),
        stripDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCStripDigi"),
        wireDigiTag = cms.InputTag("simMuonCSCDigis","MuonCSCWireDigi")
    )


    ## replacing the OLD ST algorithm with the new RU
    process.hltCscSegments = cms.EDProducer("CSCSegmentProducer",
        algo_psets = cms.VPSet(
            cms.PSet(
                algo_name = cms.string('CSCSegAlgoSK'),
                algo_psets = cms.VPSet(
                    cms.PSet(
                        chi2Max = cms.double(99999.0),
                        dPhiFineMax = cms.double(0.025),
                        dPhiMax = cms.double(0.003),
                        dRPhiFineMax = cms.double(8.0),
                        dRPhiMax = cms.double(8.0),
                        minLayersApart = cms.int32(2),
                        verboseInfo = cms.untracked.bool(True),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(99999.0),
                        dPhiFineMax = cms.double(0.025),
                        dPhiMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(3.0),
                        dRPhiMax = cms.double(8.0),
                        minLayersApart = cms.int32(2),
                        verboseInfo = cms.untracked.bool(True),
                        wideSeg = cms.double(3.0)
                    )
                ),
                chamber_types = cms.vstring(
                    'ME1/a',
                    'ME1/b',
                    'ME1/2',
                    'ME1/3',
                    'ME2/1',
                    'ME2/2',
                    'ME3/1',
                    'ME3/2',
                    'ME4/1',
                    'ME4/2'
                ),
                parameters_per_chamber_type = cms.vint32(
                    2, 1, 1, 1, 1,
                    1, 1, 1, 1, 1
                )
            ),
            cms.PSet(
                algo_name = cms.string('CSCSegAlgoTC'),
                algo_psets = cms.VPSet(
                    cms.PSet(
                        SegmentSorting = cms.int32(1),
                        chi2Max = cms.double(6000.0),
                        chi2ndfProbMin = cms.double(0.0001),
                        dPhiFineMax = cms.double(0.02),
                        dPhiMax = cms.double(0.003),
                        dRPhiFineMax = cms.double(6.0),
                        dRPhiMax = cms.double(1.2),
                        minLayersApart = cms.int32(2),
                        verboseInfo = cms.untracked.bool(True)
                    ),
                    cms.PSet(
                        SegmentSorting = cms.int32(1),
                        chi2Max = cms.double(6000.0),
                        chi2ndfProbMin = cms.double(0.0001),
                        dPhiFineMax = cms.double(0.013),
                        dPhiMax = cms.double(0.00198),
                        dRPhiFineMax = cms.double(3.0),
                        dRPhiMax = cms.double(0.6),
                        minLayersApart = cms.int32(2),
                        verboseInfo = cms.untracked.bool(True)
                    )
                ),
                chamber_types = cms.vstring(
                    'ME1/a',
                    'ME1/b',
                    'ME1/2',
                    'ME1/3',
                    'ME2/1',
                    'ME2/2',
                    'ME3/1',
                    'ME3/2',
                    'ME4/1',
                    'ME4/2'
                ),
                parameters_per_chamber_type = cms.vint32(
                    2, 1, 1, 1, 1,
                    1, 1, 1, 1, 1
                )
            ),
            cms.PSet(
                algo_name = cms.string('CSCSegAlgoDF'),
                algo_psets = cms.VPSet(
                    cms.PSet(
                        CSCSegmentDebug = cms.untracked.bool(False),
                        Pruning = cms.untracked.bool(False),
                        chi2Max = cms.double(5000.0),
                        dPhiFineMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(8.0),
                        dXclusBoxMax = cms.double(8.0),
                        dYclusBoxMax = cms.double(8.0),
                        maxDPhi = cms.double(999.0),
                        maxDTheta = cms.double(999.0),
                        maxRatioResidualPrune = cms.double(3.0),
                        minHitsForPreClustering = cms.int32(10),
                        minHitsPerSegment = cms.int32(3),
                        minLayersApart = cms.int32(2),
                        nHitsPerClusterIsShower = cms.int32(20),
                        preClustering = cms.untracked.bool(False),
                        tanPhiMax = cms.double(0.5),
                        tanThetaMax = cms.double(1.2)
                    ),
                    cms.PSet(
                        CSCSegmentDebug = cms.untracked.bool(False),
                        Pruning = cms.untracked.bool(False),
                        chi2Max = cms.double(5000.0),
                        dPhiFineMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(12.0),
                        dXclusBoxMax = cms.double(8.0),
                        dYclusBoxMax = cms.double(12.0),
                        maxDPhi = cms.double(999.0),
                        maxDTheta = cms.double(999.0),
                        maxRatioResidualPrune = cms.double(3.0),
                        minHitsForPreClustering = cms.int32(10),
                        minHitsPerSegment = cms.int32(3),
                        minLayersApart = cms.int32(2),
                        nHitsPerClusterIsShower = cms.int32(20),
                        preClustering = cms.untracked.bool(False),
                        tanPhiMax = cms.double(0.8),
                        tanThetaMax = cms.double(2.0)
                    ),
                    cms.PSet(
                        CSCSegmentDebug = cms.untracked.bool(False),
                        Pruning = cms.untracked.bool(False),
                        chi2Max = cms.double(5000.0),
                        dPhiFineMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(8.0),
                        dXclusBoxMax = cms.double(8.0),
                        dYclusBoxMax = cms.double(8.0),
                        maxDPhi = cms.double(999.0),
                        maxDTheta = cms.double(999.0),
                        maxRatioResidualPrune = cms.double(3.0),
                        minHitsForPreClustering = cms.int32(30),
                        minHitsPerSegment = cms.int32(3),
                        minLayersApart = cms.int32(2),
                        nHitsPerClusterIsShower = cms.int32(20),
                        preClustering = cms.untracked.bool(False),
                        tanPhiMax = cms.double(0.5),
                        tanThetaMax = cms.double(1.2)
                    )
                ),
                chamber_types = cms.vstring(
                    'ME1/a',
                    'ME1/b',
                    'ME1/2',
                    'ME1/3',
                    'ME2/1',
                    'ME2/2',
                    'ME3/1',
                    'ME3/2',
                    'ME4/1',
                    'ME4/2'
                ),
                parameters_per_chamber_type = cms.vint32(
                    3, 1, 2, 2, 1,
                    2, 1, 2, 1, 2
                )
            ),
            cms.PSet(
                algo_name = cms.string('CSCSegAlgoST'),
                algo_psets = cms.VPSet(
                    cms.PSet(
                        BPMinImprovement = cms.double(10000.0),
                        BrutePruning = cms.bool(True),
                        CSCDebug = cms.untracked.bool(False),
                        CorrectTheErrors = cms.bool(True),
                        Covariance = cms.double(0.0),
                        ForceCovariance = cms.bool(False),
                        ForceCovarianceAll = cms.bool(False),
                        NormChi2Cut2D = cms.double(20.0),
                        NormChi2Cut3D = cms.double(10.0),
                        Pruning = cms.bool(True),
                        SeedBig = cms.double(0.0015),
                        SeedSmall = cms.double(0.0002),
                        curvePenalty = cms.double(2.0),
                        curvePenaltyThreshold = cms.double(0.85),
                        dPhiFineMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(8.0),
                        dXclusBoxMax = cms.double(4.0),
                        dYclusBoxMax = cms.double(8.0),
                        hitDropLimit4Hits = cms.double(0.6),
                        hitDropLimit5Hits = cms.double(0.8),
                        hitDropLimit6Hits = cms.double(0.3333),
                        maxDPhi = cms.double(999.0),
                        maxDTheta = cms.double(999.0),
                        maxRatioResidualPrune = cms.double(3),
                        maxRecHitsInCluster = cms.int32(20),
                        minHitsPerSegment = cms.int32(3),
                        onlyBestSegment = cms.bool(False),
                        preClustering = cms.bool(True),
                        preClusteringUseChaining = cms.bool(True),
                        prePrun = cms.bool(True),
                        prePrunLimit = cms.double(3.17),
                        tanPhiMax = cms.double(0.5),
                        tanThetaMax = cms.double(1.2),
                        useShowering = cms.bool(False),
                        yweightPenalty = cms.double(1.5),
                        yweightPenaltyThreshold = cms.double(1.0)
                    ),
                    cms.PSet(
                        BPMinImprovement = cms.double(10000.0),
                        BrutePruning = cms.bool(True),
                        CSCDebug = cms.untracked.bool(False),
                        CorrectTheErrors = cms.bool(True),
                        Covariance = cms.double(0.0),
                        ForceCovariance = cms.bool(False),
                        ForceCovarianceAll = cms.bool(False),
                        NormChi2Cut2D = cms.double(20.0),
                        NormChi2Cut3D = cms.double(10.0),
                        Pruning = cms.bool(True),
                        SeedBig = cms.double(0.0015),
                        SeedSmall = cms.double(0.0002),
                        curvePenalty = cms.double(2.0),
                        curvePenaltyThreshold = cms.double(0.85),
                        dPhiFineMax = cms.double(0.025),
                        dRPhiFineMax = cms.double(8.0),
                        dXclusBoxMax = cms.double(4.0),
                        dYclusBoxMax = cms.double(8.0),
                        hitDropLimit4Hits = cms.double(0.6),
                        hitDropLimit5Hits = cms.double(0.8),
                        hitDropLimit6Hits = cms.double(0.3333),
                        maxDPhi = cms.double(999.0),
                        maxDTheta = cms.double(999.0),
                        maxRatioResidualPrune = cms.double(3),
                        maxRecHitsInCluster = cms.int32(24),
                        minHitsPerSegment = cms.int32(3),
                        onlyBestSegment = cms.bool(False),
                        preClustering = cms.bool(True),
                        preClusteringUseChaining = cms.bool(True),
                        prePrun = cms.bool(True),
                        prePrunLimit = cms.double(3.17),
                        tanPhiMax = cms.double(0.5),
                        tanThetaMax = cms.double(1.2),
                        useShowering = cms.bool(False),
                        yweightPenalty = cms.double(1.5),
                        yweightPenaltyThreshold = cms.double(1.0)
                    )
                ),
                chamber_types = cms.vstring(
                    'ME1/a',
                    'ME1/b',
                    'ME1/2',
                    'ME1/3',
                    'ME2/1',
                    'ME2/2',
                    'ME3/1',
                    'ME3/2',
                    'ME4/1',
                    'ME4/2'
                ),
                parameters_per_chamber_type = cms.vint32(
                    2, 1, 1, 1, 1,
                    1, 1, 1, 1, 1
                )
            ),
            cms.PSet(
                algo_name = cms.string('CSCSegAlgoRU'),
                algo_psets = cms.VPSet(
                    cms.PSet(
                        chi2Max = cms.double(100.0),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.006),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(100.0),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.005),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(100.0),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        dPhiIntMax = cms.double(0.003),
                        dPhiMax = cms.double(0.004),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(60.0),
                        chi2Norm_2D_ = cms.double(20),
                        chi2_str = cms.double(30.0),
                        dPhiIntMax = cms.double(0.002),
                        dPhiMax = cms.double(0.003),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(180.0),
                        chi2Norm_2D_ = cms.double(60),
                        chi2_str = cms.double(80.0),
                        dPhiIntMax = cms.double(0.005),
                        dPhiMax = cms.double(0.007),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    ),
                    cms.PSet(
                        chi2Max = cms.double(100.0),
                        chi2Norm_2D_ = cms.double(35),
                        chi2_str = cms.double(50.0),
                        dPhiIntMax = cms.double(0.004),
                        dPhiMax = cms.double(0.006),
                        dRIntMax = cms.double(2.0),
                        dRMax = cms.double(1.5),
                        doCollisions = cms.bool(True),
                        enlarge = cms.bool(False),
                        minLayersApart = cms.int32(1),
                        wideSeg = cms.double(3.0)
                    )
                ),
                chamber_types = cms.vstring(
                    'ME1/a',
                    'ME1/b',
                    'ME1/2',
                    'ME1/3',
                    'ME2/1',
                    'ME2/2',
                    'ME3/1',
                    'ME3/2',
                    'ME4/1',
                    'ME4/2'
                ),
                parameters_per_chamber_type = cms.vint32(
                    1, 2, 3, 4, 5,
                    6, 5, 6, 5, 6
                )
            )
        ),
        algo_type = cms.int32(5),
        inputObjects = cms.InputTag("hltCsc2DRecHits")
    )

    ## RPC
    #process.hltMuonRPCDigis = cms.EDProducer("RPCUnpackingModule",
    #    InputLabel = cms.InputTag("rawDataCollector"),
    #    doSynchro = cms.bool(False)
    #)

    process.hltRpcRecHits = cms.EDProducer("RPCRecHitProducer",
        deadSource = cms.string('File'),
        deadvecfile = cms.FileInPath('RecoLocalMuon/RPCRecHit/data/RPCDeadVec.dat'),
        maskSource = cms.string('File'),
        maskvecfile = cms.FileInPath('RecoLocalMuon/RPCRecHit/data/RPCMaskVec.dat'),
        recAlgo = cms.string('RPCRecHitStandardAlgo'),
        recAlgoConfig = cms.PSet(

        ),
        rpcDigiLabel = cms.InputTag("simMuonRPCDigis")#hltMuonRPCDigis")
    )

    process.hltGemRecHits = cms.EDProducer("GEMRecHitProducer",
                                           applyMasking = cms.bool(False),
                                           deadFile = cms.optional.FileInPath,
                                           gemDigiLabel = cms.InputTag("simMuonGEMDigis"),
                                           maskFile = cms.optional.FileInPath,
                                           mightGet = cms.optional.untracked.vstring,
                                           recAlgo = cms.string('GEMRecHitStandardAlgo'),
                                           recAlgoConfig = cms.PSet(
                                           )
                                         )

    process.hltGemSegments = cms.EDProducer("GEMSegmentProducer",
        gemRecHitLabel = cms.InputTag("hltGemRecHits"),
        algo_name = cms.string("GEMSegmentAlgorithm"),
        algo_pset = cms.PSet(
            GEMDebug = cms.untracked.bool(True),
            minHitsPerSegment = cms.uint32(2),
            preClustering = cms.bool(True),            # False => all hits in chamber are given to the fitter 
            dXclusBoxMax = cms.double(1.),             # Clstr Hit dPhi
            dYclusBoxMax = cms.double(5.),             # Clstr Hit dEta
            preClusteringUseChaining = cms.bool(True), # True ==> use Chaining() , False ==> use Clustering() Fnct
            dPhiChainBoxMax = cms.double(.02),         # Chain Hit dPhi
            dEtaChainBoxMax = cms.double(.05),         # Chain Hit dEta
            maxRecHitsInCluster = cms.int32(4),        # Does 4 make sense here?
            clusterOnlySameBXRecHits = cms.bool(True), # only working for (preClustering && preClusteringUseChaining)
        ),
    )

    process.hltMe0RecHits = cms.EDProducer("ME0RecHitProducer",
        recAlgoConfig = cms.PSet(),
        recAlgo = cms.string('ME0RecHitStandardAlgo'),
        me0DigiLabel = cms.InputTag("simMuonME0PseudoReDigis"),
    )

    process.hltMe0Segments = cms.EDProducer("ME0SegmentProducer",
        algo_psets = cms.VPSet(
            cms.PSet(
                algo_name = cms.string('ME0SegmentAlgorithm'),
                algo_pset = cms.PSet(
                    ME0Debug = cms.untracked.bool(True),
                    dEtaChainBoxMax = cms.double(0.05),
                    dPhiChainBoxMax = cms.double(0.02),
                    dTimeChainBoxMax = cms.double(15.0),
                    dXclusBoxMax = cms.double(1.0),
                    dYclusBoxMax = cms.double(5.0),
                    maxRecHitsInCluster = cms.int32(6),
                    minHitsPerSegment = cms.uint32(3),
                    preClustering = cms.bool(True),
                    preClusteringUseChaining = cms.bool(True)
                )
            ), 
            cms.PSet(
                algo_name = cms.string('ME0SegAlgoRU'),
                algo_pset = cms.PSet(
                    allowWideSegments = cms.bool(True),
                    doCollisions = cms.bool(True),
                    maxChi2Additional = cms.double(100.0),
                    maxChi2GoodSeg = cms.double(50),
                    maxChi2Prune = cms.double(50),
                    maxETASeeds = cms.double(0.1),
                    maxPhiAdditional = cms.double(0.001096605744),
                    maxPhiSeeds = cms.double(0.001096605744),
                    maxTOFDiff = cms.double(25),
                    minNumberOfHits = cms.uint32(4),
                    requireCentralBX = cms.bool(True)
                )
            )
        ),
        algo_type = cms.int32(2),
        me0RecHitLabel = cms.InputTag("hltMe0RecHits")
    )


    process.HLTMuonGemLocalRecoSequence = cms.Sequence( process.hltGemRecHits +process.hltGemSegments + process.hltMe0RecHits + process.hltMe0Segments)

    #removing unpacking for DT-CSC-RPC
    #process.hltMuonDTDigis+process.hltMuonCSCDigis+process.hltMuonRPCDigis+
    process.HLTMuonLocalRecoSequence = cms.Sequence(process.hltDt1DRecHits+process.hltDt4DSegments+process.hltCsc2DRecHits+process.hltCscSegments+ process.hltRpcRecHits + process.HLTMuonGemLocalRecoSequence )


    process.hltL2OfflineMuonSeeds = cms.EDProducer("MuonSeedGenerator",
        CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
        CSC_01 = cms.vdouble(
            0.166, 0.0, 0.0, 0.031, 0.0, 
            0.0
        ),
        CSC_01_1_scale = cms.vdouble(-1.915329, 0.0),
        CSC_02 = cms.vdouble(
            0.612, -0.207, 0.0, 0.067, -0.001, 
            0.0
        ),
        CSC_03 = cms.vdouble(
            0.787, -0.338, 0.029, 0.101, -0.008, 
            0.0
        ),
        CSC_12 = cms.vdouble(
            -0.161, 0.254, -0.047, 0.042, -0.007, 
            0.0
        ),
        CSC_12_1_scale = cms.vdouble(-6.434242, 0.0),
        CSC_12_2_scale = cms.vdouble(-1.63622, 0.0),
        CSC_12_3_scale = cms.vdouble(-1.63622, 0.0),
        CSC_13 = cms.vdouble(
            0.901, -1.302, 0.533, 0.045, 0.005, 
            0.0
        ),
        CSC_13_2_scale = cms.vdouble(-6.077936, 0.0),
        CSC_13_3_scale = cms.vdouble(-1.701268, 0.0),
        CSC_14 = cms.vdouble(
            0.606, -0.181, -0.002, 0.111, -0.003, 
            0.0
        ),
        CSC_14_3_scale = cms.vdouble(-1.969563, 0.0),
        CSC_23 = cms.vdouble(
            -0.081, 0.113, -0.029, 0.015, 0.008, 
            0.0
        ),
        CSC_23_1_scale = cms.vdouble(-19.084285, 0.0),
        CSC_23_2_scale = cms.vdouble(-6.079917, 0.0),
        CSC_24 = cms.vdouble(
            0.004, 0.021, -0.002, 0.053, 0.0, 
            0.0
        ),
        CSC_24_1_scale = cms.vdouble(-6.055701, 0.0),
        CSC_34 = cms.vdouble(
            0.062, -0.067, 0.019, 0.021, 0.003, 
            0.0
        ),
        CSC_34_1_scale = cms.vdouble(-11.520507, 0.0),
        DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
        DT_12 = cms.vdouble(
            0.183, 0.054, -0.087, 0.028, 0.002, 
            0.0
        ),
        DT_12_1_scale = cms.vdouble(-3.692398, 0.0),
        DT_12_2_scale = cms.vdouble(-3.518165, 0.0),
        DT_13 = cms.vdouble(
            0.315, 0.068, -0.127, 0.051, -0.002, 
            0.0
        ),
        DT_13_1_scale = cms.vdouble(-4.520923, 0.0),
        DT_13_2_scale = cms.vdouble(-4.257687, 0.0),
        DT_14 = cms.vdouble(
            0.359, 0.052, -0.107, 0.072, -0.004, 
            0.0
        ),
        DT_14_1_scale = cms.vdouble(-5.644816, 0.0),
        DT_14_2_scale = cms.vdouble(-4.808546, 0.0),
        DT_23 = cms.vdouble(
            0.13, 0.023, -0.057, 0.028, 0.004, 
            0.0
        ),
        DT_23_1_scale = cms.vdouble(-5.320346, 0.0),
        DT_23_2_scale = cms.vdouble(-5.117625, 0.0),
        DT_24 = cms.vdouble(
            0.176, 0.014, -0.051, 0.051, 0.003, 
            0.0
        ),
        DT_24_1_scale = cms.vdouble(-7.490909, 0.0),
        DT_24_2_scale = cms.vdouble(-6.63094, 0.0),
        DT_34 = cms.vdouble(
            0.044, 0.004, -0.013, 0.029, 0.003, 
            0.0
        ),
        DT_34_1_scale = cms.vdouble(-13.783765, 0.0),
        DT_34_2_scale = cms.vdouble(-11.901897, 0.0),
        EnableCSCMeasurement = cms.bool(True),
        EnableDTMeasurement = cms.bool(True),
        EnableME0Measurement = cms.bool(False),
        ME0RecSegmentLabel = cms.InputTag("me0Segments"),
        OL_1213 = cms.vdouble(
            0.96, -0.737, 0.0, 0.052, 0.0, 
            0.0
        ),
        OL_1213_0_scale = cms.vdouble(-4.488158, 0.0),
        OL_1222 = cms.vdouble(
            0.848, -0.591, 0.0, 0.062, 0.0, 
            0.0
        ),
        OL_1222_0_scale = cms.vdouble(-5.810449, 0.0),
        OL_1232 = cms.vdouble(
            0.184, 0.0, 0.0, 0.066, 0.0, 
            0.0
        ),
        OL_1232_0_scale = cms.vdouble(-5.964634, 0.0),
        OL_2213 = cms.vdouble(
            0.117, 0.0, 0.0, 0.044, 0.0, 
            0.0
        ),
        OL_2213_0_scale = cms.vdouble(-7.239789, 0.0),
        OL_2222 = cms.vdouble(
            0.107, 0.0, 0.0, 0.04, 0.0, 
            0.0
        ),
        OL_2222_0_scale = cms.vdouble(-7.667231, 0.0),
        SMB_10 = cms.vdouble(
            1.387, -0.038, 0.0, 0.19, 0.0, 
            0.0
        ),
        SMB_10_0_scale = cms.vdouble(2.448566, 0.0),
        SMB_11 = cms.vdouble(
            1.247, 0.72, -0.802, 0.229, -0.075, 
            0.0
        ),
        SMB_11_0_scale = cms.vdouble(2.56363, 0.0),
        SMB_12 = cms.vdouble(
            2.128, -0.956, 0.0, 0.199, 0.0, 
            0.0
        ),
        SMB_12_0_scale = cms.vdouble(2.283221, 0.0),
        SMB_20 = cms.vdouble(
            1.011, -0.052, 0.0, 0.188, 0.0, 
            0.0
        ),
        SMB_20_0_scale = cms.vdouble(1.486168, 0.0),
        SMB_21 = cms.vdouble(
            1.043, -0.124, 0.0, 0.183, 0.0, 
            0.0
        ),
        SMB_21_0_scale = cms.vdouble(1.58384, 0.0),
        SMB_22 = cms.vdouble(
            1.474, -0.758, 0.0, 0.185, 0.0, 
            0.0
        ),
        SMB_22_0_scale = cms.vdouble(1.346681, 0.0),
        SMB_30 = cms.vdouble(
            0.505, -0.022, 0.0, 0.215, 0.0, 
            0.0
        ),
        SMB_30_0_scale = cms.vdouble(-3.629838, 0.0),
        SMB_31 = cms.vdouble(
            0.549, -0.145, 0.0, 0.207, 0.0, 
            0.0
        ),
        SMB_31_0_scale = cms.vdouble(-3.323768, 0.0),
        SMB_32 = cms.vdouble(
            0.67, -0.327, 0.0, 0.22, 0.0, 
            0.0
        ),
        SMB_32_0_scale = cms.vdouble(-3.054156, 0.0),
        SME_11 = cms.vdouble(
            3.295, -1.527, 0.112, 0.378, 0.02, 
            0.0
        ),
        SME_11_0_scale = cms.vdouble(1.325085, 0.0),
        SME_12 = cms.vdouble(
            0.102, 0.599, 0.0, 0.38, 0.0, 
            0.0
        ),
        SME_12_0_scale = cms.vdouble(2.279181, 0.0),
        SME_13 = cms.vdouble(
            -1.286, 1.711, 0.0, 0.356, 0.0, 
            0.0
        ),
        SME_13_0_scale = cms.vdouble(0.104905, 0.0),
        SME_21 = cms.vdouble(
            -0.529, 1.194, -0.358, 0.472, 0.086, 
            0.0
        ),
        SME_21_0_scale = cms.vdouble(-0.040862, 0.0),
        SME_22 = cms.vdouble(
            -1.207, 1.491, -0.251, 0.189, 0.243, 
            0.0
        ),
        SME_22_0_scale = cms.vdouble(-3.457901, 0.0),
        SME_31 = cms.vdouble(
            -1.594, 1.482, -0.317, 0.487, 0.097, 
            0.0
        ),
        SME_32 = cms.vdouble(
            -0.901, 1.333, -0.47, 0.41, 0.073, 
            0.0
        ),
        SME_41 = cms.vdouble(
            -0.003, 0.005, 0.005, 0.608, 0.076, 
            0.0
        ),
        SME_42 = cms.vdouble(
            -0.003, 0.005, 0.005, 0.608, 0.076, 
            0.0
        ),
        beamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
        crackEtas = cms.vdouble(0.2, 1.6, 1.7),
        crackWindow = cms.double(0.04),
        deltaEtaCrackSearchWindow = cms.double(0.25),
        deltaEtaSearchWindow = cms.double(0.2),
        deltaPhiSearchWindow = cms.double(0.25),
        scaleDT = cms.bool(True)
    )

    # hltL2Muons are seeded by L1 GT digis and built using the DT/CSC segments
    process.hltL2MuonSeeds = cms.EDProducer("L2MuonSeedGeneratorFromL1T",
        CentralBxOnly = cms.bool(True),
        EtaMatchingBins = cms.vdouble(0.0, 2.5),
        GMTReadoutCollection = cms.InputTag(""),
        InputObjects = cms.InputTag("simGmtStage2Digis","","MYHLT"),  # cms.InputTag("hltGtStage2Digis","Muon"),
        L1MaxEta = cms.double(2.5),
        L1MinPt = cms.double(0.0),
        L1MinQuality = cms.uint32(7),
        MatchDR = cms.vdouble(0.3),
        MatchType = cms.uint32(0),
        OfflineSeedLabel = cms.untracked.InputTag("hltL2OfflineMuonSeeds"),
        Propagator = cms.string('SteppingHelixPropagatorAny'),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring('SteppingHelixPropagatorAny'),
            RPCLayers = cms.bool(True),
            UseMuonNavigation = cms.untracked.bool(True)
        ),
        SetMinPtBarrelTo = cms.double(3.5),
        SetMinPtEndcapTo = cms.double(1.0),
        SortType = cms.uint32(0),
        UseOfflineSeed = cms.untracked.bool(True),
        UseUnassociatedL1 = cms.bool(False)
    )


    process.hltL2Muons = cms.EDProducer("L2MuonProducer",
        DoSeedRefit = cms.bool(False),
        InputObjects = cms.InputTag("hltL2MuonSeeds"),
        L2TrajBuilderParameters = cms.PSet(
            BWFilterParameters = cms.PSet(
                BWSeedType = cms.string('fromGenerator'),
                CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
                DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
                EnableCSCMeasurement = cms.bool(True),
                EnableDTMeasurement = cms.bool(True),
                EnableRPCMeasurement = cms.bool(True),
                FitDirection = cms.string('outsideIn'),
                MaxChi2 = cms.double(100.0),
                MuonTrajectoryUpdatorParameters = cms.PSet(
                    ExcludeRPCFromFit = cms.bool(False),
                    Granularity = cms.int32(0),
                    MaxChi2 = cms.double(25.0),
                    RescaleError = cms.bool(False),
                    RescaleErrorFactor = cms.double(100.0),
                    UseInvalidHits = cms.bool(True)
                ),
                NumberOfSigma = cms.double(3.0),
                Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
                RPCRecSegmentLabel = cms.InputTag("hltRpcRecHits")
            ),
            DoBackwardFilter = cms.bool(True),
            DoRefit = cms.bool(False),
            DoSeedRefit = cms.bool(False),
            FilterParameters = cms.PSet(
                CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
                DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
                GEMRecSegmentLabel = cms.InputTag("hltGemRecHits"),
                ME0RecSegmentLabel = cms.InputTag("hltMe0Segments"),
                EnableCSCMeasurement = cms.bool(True),
                EnableDTMeasurement = cms.bool(True),
                EnableRPCMeasurement = cms.bool(True),
                EnableGEMMeasurement = cms.bool(True),
                EnableME0Measurement = cms.bool(True),
                FitDirection = cms.string('insideOut'),
                MaxChi2 = cms.double(1000.0),
                MuonTrajectoryUpdatorParameters = cms.PSet(
                    ExcludeRPCFromFit = cms.bool(False),
                    Granularity = cms.int32(0),
                    MaxChi2 = cms.double(25.0),
                    RescaleError = cms.bool(False),
                    RescaleErrorFactor = cms.double(100.0),
                    UseInvalidHits = cms.bool(True)
                ),
                NumberOfSigma = cms.double(3.0),
                Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
                RPCRecSegmentLabel = cms.InputTag("hltRpcRecHits")
            ),
            NavigationType = cms.string('Standard'),
            SeedPosition = cms.string('in'),
            SeedPropagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            SeedTransformerParameters = cms.PSet(
                Fitter = cms.string('hltESPKFFittingSmootherForL2Muon'),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                NMinRecHits = cms.uint32(2),
                Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
                RescaleError = cms.double(100.0),
                UseSubRecHits = cms.bool(False)
            )
        ),
        MuonTrajectoryBuilder = cms.string('Exhaustive'),
        SeedTransformerParameters = cms.PSet(
            Fitter = cms.string('hltESPKFFittingSmootherForL2Muon'),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            NMinRecHits = cms.uint32(2),
            Propagator = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            RescaleError = cms.double(100.0),
            UseSubRecHits = cms.bool(False)
        ),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring(
                'hltESPFastSteppingHelixPropagatorAny', 
                'hltESPFastSteppingHelixPropagatorOpposite'
            ),
            RPCLayers = cms.bool(True),
            UseMuonNavigation = cms.untracked.bool(True)
        ),
        TrackLoaderParameters = cms.PSet(
            DoSmoothing = cms.bool(False),
            MuonUpdatorAtVertexParameters = cms.PSet(
                BeamSpotPosition = cms.vdouble(0.0, 0.0, 0.0),
                BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
                MaxChi2 = cms.double(1000000.0),
                Propagator = cms.string('hltESPFastSteppingHelixPropagatorOpposite')
            ),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            VertexConstraint = cms.bool(True),
            beamSpot = cms.InputTag("hltOnlineBeamSpot")
        )
    )


    process.HLTL2muonrecoNocandSequence = cms.Sequence(process.HLTMuonLocalRecoSequence+
                                                       process.hltL2OfflineMuonSeeds+
                                                       process.hltL2MuonSeeds+
                                                       process.hltL2Muons
    )

    process.hltL2MuonCandidates = cms.EDProducer("L2MuonCandidateProducer",
                                                 InputObjects = cms.InputTag("hltL2Muons","UpdatedAtVtx")
                                               )


    process.HLTL2muonrecoSequence = cms.Sequence(process.HLTL2muonrecoNocandSequence+
                                                 process.hltL2MuonCandidates)


    #########################################
    ### L3 Muon Reco processes
    #########################################

    #### naming of processes is the one used in the muon HLT modules

    #### localPixelReco
    process.hltSiPixelClusters = cms.EDProducer("SiPixelClusterProducer",
        ChannelThreshold = cms.int32(1000),
        ClusterThreshold = cms.int32(4000),
        ClusterThreshold_L1 = cms.int32(4000),
        ElectronPerADCGain = cms.double(600.0),
        MissCalibrate = cms.bool(False),
        Phase2Calibration = cms.bool(True),
        Phase2DigiBaseline = cms.double(1200.0),
        Phase2KinkADC = cms.int32(8),
        Phase2ReadoutMode = cms.int32(-1),
        SeedThreshold = cms.int32(1000),
        SplitClusters = cms.bool(False),
        VCaltoElectronGain = cms.int32(65),
        VCaltoElectronGain_L1 = cms.int32(65),
        VCaltoElectronOffset = cms.int32(-414),
        VCaltoElectronOffset_L1 = cms.int32(-414),
        maxNumberOfClusters = cms.int32(-1),
        payloadType = cms.string('Offline'),
        src = cms.InputTag("simSiPixelDigis","Pixel")
    )

    process.hltSiPixelClustersCache = cms.EDProducer("SiPixelClusterShapeCacheProducer",
        onDemand = cms.bool(False),
        src = cms.InputTag("hltSiPixelClusters")
    )

    process.hltSiPixelRecHits = cms.EDProducer("SiPixelRecHitConverter",
        CPE = cms.string('PixelCPEGeneric'), 
        VerboseLevel = cms.untracked.int32(0),
        src = cms.InputTag("hltSiPixelClusters")
    )


    process.HLTDoLocalPixelSequence = cms.Sequence(process.hltSiPixelClusters+process.hltSiPixelClustersCache+process.hltSiPixelRecHits)

    #### localStripsReco
    process.hltSiStripClusters = cms.EDProducer("MeasurementTrackerEventProducer",
        Phase2TrackerCluster1DProducer = cms.string('siPhase2Clusters'), 
        badPixelFEDChannelCollectionLabels = cms.VInputTag("siPixelDigis"),
        inactivePixelDetectorLabels = cms.VInputTag(),
        inactiveStripDetectorLabels = cms.VInputTag("siStripDigis"),
        measurementTracker = cms.string(''),
        pixelCablingMapLabel = cms.string(''),
        pixelClusterProducer = cms.string('hltSiPixelClusters'),
        skipClusters = cms.InputTag(""),
        stripClusterProducer = cms.string(''),
        switchOffPixelsIfEmpty = cms.bool(True)
    )

    process.HLTDoLocalStripSequence = cms.Sequence(process.siPhase2Clusters+process.hltSiStripClusters) 


    #### OutsideIn L3
    process.hltIterL3OISeedsFromL2Muons = cms.EDProducer("TSGForOIFromL2",
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        SF1 = cms.double(3.0),
        SF2 = cms.double(4.0),
        SF3 = cms.double(5.0),
        SF4 = cms.double(7.0),
        SF5 = cms.double(10.0),
        SF6 = cms.double(2.0),
        UseHitLessSeeds = cms.bool(True),
        adjustErrorsDynamicallyForHitless = cms.bool(True),
        adjustErrorsDynamicallyForHits = cms.bool(False),
        debug = cms.untracked.bool(False),
        estimator = cms.string('hltESPChi2MeasurementEstimator100'),
        eta1 = cms.double(0.2),
        eta2 = cms.double(0.3),
        eta3 = cms.double(1.0),
        eta4 = cms.double(1.2),
        eta5 = cms.double(1.6),
        eta6 = cms.double(1.4),
        eta7 = cms.double(2.1),
        fixedErrorRescaleFactorForHitless = cms.double(2.0),
        fixedErrorRescaleFactorForHits = cms.double(1.0),
        hitsToTry = cms.int32(1),
        layersToTry = cms.int32(2),
        maxEtaForTOB = cms.double(1.8),
        maxHitSeeds = cms.uint32(1),
        maxHitlessSeeds = cms.uint32(5),
        maxSeeds = cms.uint32(20),
        minEtaForTEC = cms.double(0.7),
        numL2ValidHitsCutAllEndcap = cms.uint32(30),
        numL2ValidHitsCutAllEta = cms.uint32(20),
        pT1 = cms.double(13.0),
        pT2 = cms.double(30.0),
        pT3 = cms.double(70.0),
        propagatorName = cms.string('PropagatorWithMaterialParabolicMf'),
        src = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
        tsosDiff1 = cms.double(0.2),
        tsosDiff2 = cms.double(0.02)
    )


    process.hltIterL3OITrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string(''),
        TrajectoryBuilder = cms.string('CkfTrajectoryBuilder'),
        TrajectoryBuilderPSet = cms.PSet(
           refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryBuilder')
        ),
        TrajectoryCleaner = cms.string('muonSeededTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterial'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(False),
        maxNSeeds = cms.uint32(500000),
        maxSeedsBeforeCleaning = cms.uint32(5000),
        src = cms.InputTag("hltIterL3OISeedsFromL2Muons"),
        useHitsSplitting = cms.bool(False)
    )


    process.hltIterL3OIMuCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('iter10'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIterL3OITrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.hltIterL3OIMuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(True),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
                d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
                dr_exp = cms.vint32(4, 4, 2147483647),
                dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 2147483647),
                dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
            ),
            maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            maxChi2n = cms.vdouble(10.0, 1.0, 0.4),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
            maxLostLayers = cms.vint32(4, 3, 2),
            min3DLayers = cms.vint32(1, 2, 1),
            minLayers = cms.vint32(3, 5, 5),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 1)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks"),
        vertices = cms.InputTag("Notused")
    )


    process.hltIterL3OIMuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIterL3OIMuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIterL3OIMuCtfWithMaterialTracks")
    )


    process.hltL3MuonsIterL3OI = cms.EDProducer("L3MuonProducer",
        L3TrajBuilderParameters = cms.PSet(
            GlbRefitterParameters = cms.PSet(
                CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
                Chi2CutCSC = cms.double(150.0),
                Chi2CutDT = cms.double(10.0),
                Chi2CutRPC = cms.double(1.0),
                DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
                DYTthrs = cms.vint32(30, 15),
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                HitThreshold = cms.int32(1),
                MuonHitsOption = cms.int32(1),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                PropDirForCosmics = cms.bool(False),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitFlag = cms.bool(True),
                RefitRPCHits = cms.bool(True),
                SkipStation = cms.int32(-1),
                TrackerRecHitBuilder = cms.string('WithTrackAngle'),
                TrackerSkipSection = cms.int32(-1),
                TrackerSkipSystem = cms.int32(-1)
            ),
            GlobalMuonTrackMatcher = cms.PSet(
                Chi2Cut_1 = cms.double(50.0),
                Chi2Cut_2 = cms.double(50.0),
                Chi2Cut_3 = cms.double(200.0),
                DeltaDCut_1 = cms.double(40.0),
                DeltaDCut_2 = cms.double(10.0),
                DeltaDCut_3 = cms.double(15.0),
                DeltaRCut_1 = cms.double(0.1),
                DeltaRCut_2 = cms.double(0.2),
                DeltaRCut_3 = cms.double(1.0),
                Eta_threshold = cms.double(1.2),
                LocChi2Cut = cms.double(0.001),
                MinP = cms.double(2.5),
                MinPt = cms.double(1.0),
                Propagator = cms.string('hltESPSmartPropagator'),
                Pt_threshold1 = cms.double(0.0),
                Pt_threshold2 = cms.double(999999999.0),
                Quality_1 = cms.double(20.0),
                Quality_2 = cms.double(15.0),
                Quality_3 = cms.double(7.0)
            ),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            MuonTrackingRegionBuilder = cms.PSet(
                DeltaEta = cms.double(0.2),
                DeltaPhi = cms.double(0.15),
                DeltaR = cms.double(0.025),
                DeltaZ = cms.double(24.2),
                EtaR_UpperLimit_Par1 = cms.double(0.25),
                EtaR_UpperLimit_Par2 = cms.double(0.15),
                Eta_fixed = cms.bool(True),
                Eta_min = cms.double(0.1),
                MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
                OnDemand = cms.int32(-1),
                PhiR_UpperLimit_Par1 = cms.double(0.6),
                PhiR_UpperLimit_Par2 = cms.double(0.2),
                Phi_fixed = cms.bool(True),
                Phi_min = cms.double(0.1),
                Pt_fixed = cms.bool(False),
                Pt_min = cms.double(3.0),
                Rescale_Dz = cms.double(4.0),
                Rescale_eta = cms.double(3.0),
                Rescale_phi = cms.double(3.0),
                UseVertex = cms.bool(False),
                Z_fixed = cms.bool(False),
                beamSpot = cms.InputTag("hltOnlineBeamSpot"),
                input = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
                maxRegions = cms.int32(2),
                precise = cms.bool(True),
                vertexCollection = cms.InputTag("pixelVertices")
            ),
            PCut = cms.double(2.5),
            PtCut = cms.double(1.0),
            RefitRPCHits = cms.bool(True),
            ScaleTECxFactor = cms.double(-1.0),
            ScaleTECyFactor = cms.double(-1.0),
            TrackTransformer = cms.PSet(
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitRPCHits = cms.bool(True),
                Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
                TrackerRecHitBuilder = cms.string('WithTrackAngle')
            ),
            TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
            TrackerRecHitBuilder = cms.string('WithTrackAngle'),
            tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
            tkTrajLabel = cms.InputTag("hltIterL3OIMuonTrackSelectionHighPurity"),
            tkTrajMaxChi2 = cms.double(9999.0),
            tkTrajMaxDXYBeamSpot = cms.double(9999.0),
            tkTrajUseVertex = cms.bool(False),
            tkTrajVertex = cms.InputTag("Notused")
        ),
        MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring(
                'hltESPSmartPropagatorAny', 
                'SteppingHelixPropagatorAny', 
                'hltESPSmartPropagator', 
                'hltESPSteppingHelixPropagatorOpposite'
            ),
            RPCLayers = cms.bool(True),
            UseMuonNavigation = cms.untracked.bool(True)
        ),
        TrackLoaderParameters = cms.PSet(
            DoSmoothing = cms.bool(True),
            MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
            MuonUpdatorAtVertexParameters = cms.PSet(
                BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
                MaxChi2 = cms.double(1000000.0),
                Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
            ),
            PutTkTrackIntoEvent = cms.untracked.bool(False),
            SmoothTkTrack = cms.untracked.bool(False),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            VertexConstraint = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot")
        )
    )


    process.HLTIterL3OImuonTkCandidateSequence = cms.Sequence(process.hltIterL3OISeedsFromL2Muons+
                                                              process.hltIterL3OITrackCandidates+
                                                              process.hltIterL3OIMuCtfWithMaterialTracks+
                                                              process.hltIterL3OIMuonTrackCutClassifier+
                                                              process.hltIterL3OIMuonTrackSelectionHighPurity+
                                                              process.hltL3MuonsIterL3OI)


    process.hltIterL3OIL3MuonsLinksCombination = cms.EDProducer("L3TrackLinksCombiner",
        labels = cms.VInputTag("hltL3MuonsIterL3OI")
    )

    process.hltIterL3OIL3Muons = cms.EDProducer("L3TrackCombiner",
        labels = cms.VInputTag("hltL3MuonsIterL3OI")
    )

    process.hltIterL3OIL3MuonCandidates = cms.EDProducer("L3MuonCandidateProducer",
        InputLinksObjects = cms.InputTag("hltIterL3OIL3MuonsLinksCombination"),
        InputObjects = cms.InputTag("hltIterL3OIL3Muons"),
        MuonPtOption = cms.string('Tracker')
    )




    #### InsideOut L3 seeded by L2
    process.hltL2SelectorForL3IO = cms.EDProducer("HLTMuonL2SelectorForL3IO",
        InputLinks = cms.InputTag("hltIterL3OIL3MuonsLinksCombination"),
        MaxNormalizedChi2 = cms.double(20.0),
        MaxPtDifference = cms.double(0.3),
        MinNhits = cms.int32(1),
        MinNmuonHits = cms.int32(1),
        applyL3Filters = cms.bool(False),
        l2Src = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
        l3OISrc = cms.InputTag("hltIterL3OIL3MuonCandidates")
    )

    process.hltIterL3MuonPixelTracksFilter = cms.EDProducer("PixelTrackFilterByKinematicsProducer",
        chi2 = cms.double(1000.0),
        nSigmaInvPtTolerance = cms.double(0.0),
        nSigmaTipMaxTolerance = cms.double(0.0),
        ptMin = cms.double(0.9),  
        tipMax = cms.double(1.0)
    )

    process.hltIterL3MuonPixelTracksFitter = cms.EDProducer("PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool(False),
        scaleFactor = cms.double(0.65)
    )

    process.hltIterL3MuonPixelTracksTrackingRegions = cms.EDProducer("MuonTrackingRegionEDProducer",
        DeltaEta = cms.double(0.2),
        DeltaPhi = cms.double(0.15),
        DeltaR = cms.double(0.025),
        DeltaZ = cms.double(24.2),
        EtaR_UpperLimit_Par1 = cms.double(0.25),
        EtaR_UpperLimit_Par2 = cms.double(0.15),
        Eta_fixed = cms.bool(True),
        Eta_min = cms.double(0.0),
        MeasurementTrackerName = cms.InputTag(""),
        OnDemand = cms.int32(-1),
        PhiR_UpperLimit_Par1 = cms.double(0.6),
        PhiR_UpperLimit_Par2 = cms.double(0.2),
        Phi_fixed = cms.bool(True),
        Phi_min = cms.double(0.0),
        Pt_fixed = cms.bool(True),
        Pt_min = cms.double(2.0),
        Rescale_Dz = cms.double(4.0),
        Rescale_eta = cms.double(3.0),
        Rescale_phi = cms.double(3.0),
        UseVertex = cms.bool(False),
        Z_fixed = cms.bool(True),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        input = cms.InputTag("hltL2SelectorForL3IO"),
        maxRegions = cms.int32(5),
        precise = cms.bool(True),
        vertexCollection = cms.InputTag("notUsed")
    )

    ##### Check how many layers we actually need!!!!
    ##### Muons can run with the Run2 number of layers until we don't trigger above 2.4 (L1TkMuons)
    process.hltIterL3MuonPixelLayerQuadruplets = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),      
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4', 
            'BPix1+BPix2+BPix3+FPix1_pos', 
            'BPix1+BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos+FPix2_pos', 
            'BPix1+BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos', 
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg', 
            #'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos', 
            #'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg', 
            #'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos', 
            #'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg', 
            #'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos', 
            #'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg', 
            #'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos', 
            #'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg', 
            #'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos', 
            #'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )


    process.hltIterL3MuonPixelTracksHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag(""),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(0),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("hltIterL3MuonPixelLayerQuadruplets"),
        trackingRegions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )

    process.hltIterL3MuonPixelTracksHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0.0),
        CAPhiCut = cms.double(0.2),
        CAThetaCut = cms.double(0.005),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("hltSiPixelClustersCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("hltIterL3MuonPixelTracksHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.7),
            pt2 = cms.double(2.0),
            value1 = cms.double(200.0),
            value2 = cms.double(50.0)
        ),
        useBendingCorrection = cms.bool(True)
    )

    process.hltIterL3MuonPixelTracks = cms.EDProducer("PixelTrackProducer",
        Cleaner = cms.string('hltPixelTracksCleanerBySharedHits'),
        Filter = cms.InputTag("hltIterL3MuonPixelTracksFilter"),
        Fitter = cms.InputTag("hltIterL3MuonPixelTracksFitter"),
        SeedingHitSets = cms.InputTag("hltIterL3MuonPixelTracksHitQuadruplets"),
        passLabel = cms.string('')
    )

    process.hltIterL3MuonPixelVertices = cms.EDProducer("PixelVertexProducer",
        Finder = cms.string('DivisiveVertexFinder'),
        Method2 = cms.bool(True),
        NTrkMin = cms.int32(2),
        PVcomparer = cms.PSet(
            refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
        ),
        PtMin = cms.double(1.0),
        TrackCollection = cms.InputTag("hltIterL3MuonPixelTracks"),
        UseError = cms.bool(True),
        Verbosity = cms.int32(0),
        WtAverage = cms.bool(True),
        ZOffset = cms.double(5.0),
        ZSeparation = cms.double(0.05),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )

    process.hltIterL3MuonTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
        PVcomparer = cms.PSet(
            refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
        ),
        fractionSumPt2 = cms.double(0.3),
        maxVtx = cms.uint32(100),
        minSumPt2 = cms.double(0.0),
        src = cms.InputTag("hltIterL3MuonPixelVertices")
    )

    process.HLTIterL3MuonRecoPixelTracksSequence = cms.Sequence(process.hltIterL3MuonPixelTracksFilter+
                                                                process.hltIterL3MuonPixelTracksFitter+
                                                                process.hltIterL3MuonPixelTracksTrackingRegions+
                                                                process.hltIterL3MuonPixelLayerQuadruplets+
                                                                process.hltIterL3MuonPixelTracksHitDoublets+
                                                                process.hltIterL3MuonPixelTracksHitQuadruplets+
                                                                process.hltIterL3MuonPixelTracks)


    #### iteration 0 for the inside-out
    process.hltIter0IterL3MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("hltIterL3MuonPixelTracks"),
        InputVertexCollection = cms.InputTag("hltIterL3MuonTrimmedPixelVertices"),
        SeedCreatorPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2SeedFromProtoTracks')
        ),
        TTRHBuilder = cms.string('WithTrackAngle'),
        originHalfLength = cms.double(0.3),
        originRadius = cms.double(0.1),
        useEventsWithNoVertex = cms.bool(True),
        usePV = cms.bool(False),
        useProtoTrackKinematics = cms.bool(False)
    )

    process.hltIter0IterL3MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('none'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT')
        ),
        TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(True),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        src = cms.InputTag("hltIter0IterL3MuonPixelSeedsFromPixelTracks"),
        useHitsSplitting = cms.bool(True)
    )


    process.hltIter0IterL3MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('hltIter0'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIter0IterL3MuonCkfTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.hltIter0IterL3MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
                d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
                dr_exp = cms.vint32(4, 4, 2147483647),
                dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 2147483647),
                dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
            ),
            maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
            maxLostLayers = cms.vint32(1, 1, 1),
            min3DLayers = cms.vint32(0, 3, 4),
            minLayers = cms.vint32(3, 3, 4),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 3, 4)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracks"),
        vertices = cms.InputTag("hltIterL3MuonTrimmedPixelVertices")
    )


    process.hltIter0IterL3MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0IterL3MuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIter0IterL3MuonCtfWithMaterialTracks")
    )

    process.HLTIterativeTrackingIteration0ForIterL3Muon = cms.Sequence(
        process.hltIter0IterL3MuonPixelSeedsFromPixelTracks+
        process.hltIter0IterL3MuonCkfTrackCandidates+
        process.hltIter0IterL3MuonCtfWithMaterialTracks+
        process.hltIter0IterL3MuonTrackCutClassifier+
        process.hltIter0IterL3MuonTrackSelectionHighPurity)

    #### iteration 2
    process.hltIter2IterL3MuonClustersRefRemoval = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(16.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(""),
        overrideTrkQuals = cms.InputTag(""),
        phase2pixelClusters = cms.InputTag("hltSiPixelClusters"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity")
    )

    process.hltIter2IterL3MuonMaskedMeasurementTrackerEvent = cms.EDProducer("MaskedMeasurementTrackerEventProducer",
        OnDemand = cms.bool(False),
        phase2clustersToSkip = cms.InputTag("hltIter2IterL3MuonClustersRefRemoval"),
        src = cms.InputTag("hltSiStripClusters")
    )

    process.hltIter2IterL3MuonPixelLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltIter2IterL3MuonClustersRefRemoval"),
         ),
        FPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltIter2IterL3MuonClustersRefRemoval"),
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3', 
            'BPix2+BPix3+BPix4', 
            'BPix1+BPix3+BPix4', 
            'BPix1+BPix2+BPix4', 
            'BPix2+BPix3+FPix1_pos', 
            'BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos', 
            'BPix1+BPix2+FPix1_neg', 
            'BPix2+FPix1_pos+FPix2_pos', 
            'BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos', 
            'BPix1+FPix1_neg+FPix2_neg', 
            'FPix1_pos+FPix2_pos+FPix3_pos', 
            'FPix1_neg+FPix2_neg+FPix3_neg', 
            'BPix1+BPix3+FPix1_pos', 
            'BPix1+BPix2+FPix2_pos', 
            'BPix1+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix2_neg', 
            'BPix1+FPix2_neg+FPix3_neg', 
            'BPix1+FPix1_neg+FPix3_neg', 
            'BPix1+FPix2_pos+FPix3_pos', 
            'BPix1+FPix1_pos+FPix3_pos'
        )
    )

    process.hltIter2IterL3MuonPixelClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
        ClusterCollectionLabel = cms.InputTag("hltSiStripClusters"),
        MaxNumberOfCosmicClusters = cms.uint32(50000),
        MaxNumberOfPixelClusters = cms.uint32(10000),
        PixelClusterCollectionLabel = cms.InputTag("hltSiPixelClusters"),
        cut = cms.string(''),
        doClusterCheck = cms.bool(False),
        silentClusterCheck = cms.untracked.bool(False)
    )


    process.hltIter2IterL3MuonPixelHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("hltIter2IterL3MuonPixelClusterCheck"),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(0),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("hltIter2IterL3MuonPixelLayerTriplets"),
        trackingRegions = cms.InputTag("hltIterL3MuonPixelTracksTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )


    process.hltIter2IterL3MuonPixelHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
        CAHardPtCut = cms.double(0.3),
        CAPhiCut = cms.double(0.1),
        CAThetaCut = cms.double(0.015),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        doublets = cms.InputTag("hltIter2IterL3MuonPixelHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(8.0),
            value1 = cms.double(100.0),
            value2 = cms.double(6.0)
        ),
        useBendingCorrection = cms.bool(True)
    )


    process.hltIter2IterL3MuonPixelSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer",
        MinOneOverPtError = cms.double(1.0),
        OriginTransverseErrorMultiplier = cms.double(1.0),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5.0),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string('ParabolicMf'),
        propagator = cms.string('PropagatorWithMaterialParabolicMf'),
        seedingHitSets = cms.InputTag("hltIter2IterL3MuonPixelHitTriplets")
    )

    process.hltIter2IterL3MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltIter2IterL3MuonMaskedMeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string(''),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('HLTIter2IterL3MuonPSetGroupedCkfTrajectoryBuilderIT')
        ),
        TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(False),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        src = cms.InputTag("hltIter2IterL3MuonPixelSeeds"),
        useHitsSplitting = cms.bool(False)
    )

    process.hltIter2IterL3MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('hltIter2'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltIter2IterL3MuonMaskedMeasurementTrackerEvent"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIter2IterL3MuonCkfTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.hltIter2IterL3MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
                d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
                dr_exp = cms.vint32(4, 4, 2147483647),
                dr_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
                dr_par2 = cms.vdouble(3.40282346639e+38, 0.3, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 2147483647),
                dz_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
                dz_par2 = cms.vdouble(3.40282346639e+38, 0.35, 3.40282346639e+38)
            ),
            maxChi2 = cms.vdouble(9999.0, 25.0, 3.40282346639e+38),
            maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
            maxLostLayers = cms.vint32(1, 1, 1),
            min3DLayers = cms.vint32(0, 0, 0),
            minLayers = cms.vint32(3, 3, 3),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 0)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIter2IterL3MuonCtfWithMaterialTracks"),
        vertices = cms.InputTag("hltIterL3MuonTrimmedPixelVertices")
    )


    process.hltIter2IterL3MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter2IterL3MuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIter2IterL3MuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIter2IterL3MuonCtfWithMaterialTracks")
    )

    process.HLTIterativeTrackingIteration2ForIterL3Muon = cms.Sequence(
        process.hltIter2IterL3MuonClustersRefRemoval+
        process.hltIter2IterL3MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3MuonPixelLayerTriplets+
        process.hltIter2IterL3MuonPixelClusterCheck+
        process.hltIter2IterL3MuonPixelHitDoublets+
        process.hltIter2IterL3MuonPixelHitTriplets+
        process.hltIter2IterL3MuonPixelSeeds+
        process.hltIter2IterL3MuonCkfTrackCandidates+
        process.hltIter2IterL3MuonCtfWithMaterialTracks+
        process.hltIter2IterL3MuonTrackCutClassifier+
        process.hltIter2IterL3MuonTrackSelectionHighPurity)


    ##### muon merged from iter0 and iter2
    process.hltIter2IterL3MuonMerged = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(20.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("hltIter0IterL3MuonTrackSelectionHighPurity", "hltIter2IterL3MuonTrackSelectionHighPurity"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag("hltIter0IterL3MuonTrackSelectionHighPurity", "hltIter2IterL3MuonTrackSelectionHighPurity"),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(False),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    process.hltL3MuonsIterL3IO = cms.EDProducer("L3MuonProducer",
        L3TrajBuilderParameters = cms.PSet(
            GlbRefitterParameters = cms.PSet(
                CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
                Chi2CutCSC = cms.double(150.0),
                Chi2CutDT = cms.double(10.0),
                Chi2CutRPC = cms.double(1.0),
                DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
                DYTthrs = cms.vint32(30, 15),
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                HitThreshold = cms.int32(1),
                MuonHitsOption = cms.int32(1),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                PropDirForCosmics = cms.bool(False),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitFlag = cms.bool(True),
                RefitRPCHits = cms.bool(True),
                SkipStation = cms.int32(-1),
                TrackerRecHitBuilder = cms.string('WithTrackAngle'),
                TrackerSkipSection = cms.int32(-1),
                TrackerSkipSystem = cms.int32(-1)
            ),
            GlobalMuonTrackMatcher = cms.PSet(
                Chi2Cut_1 = cms.double(50.0),
                Chi2Cut_2 = cms.double(50.0),
                Chi2Cut_3 = cms.double(200.0),
                DeltaDCut_1 = cms.double(40.0),
                DeltaDCut_2 = cms.double(10.0),
                DeltaDCut_3 = cms.double(15.0),
                DeltaRCut_1 = cms.double(0.1),
                DeltaRCut_2 = cms.double(0.2),
                DeltaRCut_3 = cms.double(1.0),
                Eta_threshold = cms.double(1.2),
                LocChi2Cut = cms.double(0.001),
                MinP = cms.double(2.5),
                MinPt = cms.double(1.0),
                Propagator = cms.string('hltESPSmartPropagator'),
                Pt_threshold1 = cms.double(0.0),
                Pt_threshold2 = cms.double(999999999.0),
                Quality_1 = cms.double(20.0),
                Quality_2 = cms.double(15.0),
                Quality_3 = cms.double(7.0)
            ),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            MuonTrackingRegionBuilder = cms.PSet(
                DeltaEta = cms.double(0.04),
                DeltaPhi = cms.double(0.15),
                DeltaR = cms.double(0.025),
                DeltaZ = cms.double(24.2),
                EtaR_UpperLimit_Par1 = cms.double(0.25),
                EtaR_UpperLimit_Par2 = cms.double(0.15),
                Eta_fixed = cms.bool(True),
                Eta_min = cms.double(0.1),
                MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
                OnDemand = cms.int32(-1),
                PhiR_UpperLimit_Par1 = cms.double(0.6),
                PhiR_UpperLimit_Par2 = cms.double(0.2),
                Phi_fixed = cms.bool(True),
                Phi_min = cms.double(0.1),
                Pt_fixed = cms.bool(True),
                Pt_min = cms.double(3.0),
                Rescale_Dz = cms.double(4.0),
                Rescale_eta = cms.double(3.0),
                Rescale_phi = cms.double(3.0),
                UseVertex = cms.bool(False),
                Z_fixed = cms.bool(True),
                beamSpot = cms.InputTag("hltOnlineBeamSpot"),
                input = cms.InputTag("hltL2SelectorForL3IO"),
                maxRegions = cms.int32(2),
                precise = cms.bool(True),
                vertexCollection = cms.InputTag("pixelVertices")
            ),
            PCut = cms.double(2.5),
            PtCut = cms.double(1.0),
            RefitRPCHits = cms.bool(True),
            ScaleTECxFactor = cms.double(-1.0),
            ScaleTECyFactor = cms.double(-1.0),
            TrackTransformer = cms.PSet(
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitRPCHits = cms.bool(True),
                Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
                TrackerRecHitBuilder = cms.string('WithTrackAngle')
            ),
            TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
            TrackerRecHitBuilder = cms.string('WithTrackAngle'),
            matchToSeeds = cms.bool(True),
            tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
            tkTrajLabel = cms.InputTag("hltIter2IterL3MuonMerged"),
            tkTrajMaxChi2 = cms.double(9999.0),
            tkTrajMaxDXYBeamSpot = cms.double(9999.0),
            tkTrajUseVertex = cms.bool(False),
            tkTrajVertex = cms.InputTag("hltIterL3MuonPixelVertices")
        ),
        MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring(
                'hltESPSmartPropagatorAny', 
                'SteppingHelixPropagatorAny', 
                'hltESPSmartPropagator', 
                'hltESPSteppingHelixPropagatorOpposite'
            ),
            RPCLayers = cms.bool(True),
            UseMuonNavigation = cms.untracked.bool(True)
        ),
        TrackLoaderParameters = cms.PSet(
            DoSmoothing = cms.bool(False),
            MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
            MuonUpdatorAtVertexParameters = cms.PSet(
                BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
                MaxChi2 = cms.double(1000000.0),
                Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
            ),
            PutTkTrackIntoEvent = cms.untracked.bool(False),
            SmoothTkTrack = cms.untracked.bool(False),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            VertexConstraint = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot")
        )
    )


    process.hltIterL3MuonsFromL2LinksCombination = cms.EDProducer("L3TrackLinksCombiner",
                                                                  labels = cms.VInputTag("hltL3MuonsIterL3OI", "hltL3MuonsIterL3IO")
    )


    #### InsideOut seeded by L1 which are not giving a L2

    process.hltIterL3MuonL1MuonNoL2Selector = cms.EDProducer( "HLTL1MuonNoL2Selector",
        SeedMapTag = cms.InputTag( "hltL2Muons" ),
        L1MinPt = cms.double( -1.0 ),
        CentralBxOnly = cms.bool( True ),
        InputObjects = cms.InputTag("simGmtStage2Digis","","MYHLT"),  # cms.InputTag( 'hltGtStage2Digis','Muon' ),
        L2CandTag = cms.InputTag( "hltL2MuonCandidates" ),
        L1MaxEta = cms.double( 5.0 ),
        L1MinQuality = cms.uint32( 7 )
    )

    process.hltIterL3FromL1MuonPixelTracksTrackingRegions = cms.EDProducer( "CandidateSeededTrackingRegionsEDProducer",
        RegionPSet = cms.PSet( 
          vertexCollection = cms.InputTag( "notUsed" ),
          zErrorVetex = cms.double( 0.2 ),
          beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
          zErrorBeamSpot = cms.double( 24.2 ),
          maxNVertices = cms.int32( 1 ),
          maxNRegions = cms.int32( 2 ),
          nSigmaZVertex = cms.double( 3.0 ),
          nSigmaZBeamSpot = cms.double( 4.0 ),
          ptMin = cms.double( 10.0 ),
          mode = cms.string( "BeamSpotSigma" ),
          input = cms.InputTag( "hltIterL3MuonL1MuonNoL2Selector" ),
          searchOpt = cms.bool( False ),
          whereToUseMeasurementTracker = cms.string( "Never" ),
          originRadius = cms.double( 0.2 ),
          measurementTrackerName = cms.InputTag( "" ),
          precise = cms.bool( True ),
          deltaEta = cms.double( 0.35 ),
          deltaPhi = cms.double( 0.2 )
        )
    )

    process.hltIterL3FromL1MuonPixelLayerQuadruplets = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4', 
            'BPix1+BPix2+BPix3+FPix1_pos', 
            'BPix1+BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos+FPix2_pos', 
            'BPix1+BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos', 
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg'
        )
    )


    process.hltIterL3FromL1MuonPixelTracksHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag(""),
        layerPairs = cms.vuint32(0, 1, 2),
        maxElement = cms.uint32(0),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("hltIterL3FromL1MuonPixelLayerQuadruplets"),
        trackingRegions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )


    process.hltIterL3FromL1MuonPixelTracksHitQuadruplets = cms.EDProducer("CAHitQuadrupletEDProducer",
        CAHardPtCut = cms.double(0.0),
        CAPhiCut = cms.double(0.2),
        CAThetaCut = cms.double(0.005),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('LowPtClusterShapeSeedComparitor'),
            clusterShapeCacheSrc = cms.InputTag("hltSiPixelClustersCache"),
            clusterShapeHitFilter = cms.string('ClusterShapeHitFilter')
        ),
        doublets = cms.InputTag("hltIterL3FromL1MuonPixelTracksHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        fitFastCircle = cms.bool(True),
        fitFastCircleChi2Cut = cms.bool(True),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.7),
            pt2 = cms.double(2.0),
            value1 = cms.double(200.0),
            value2 = cms.double(50.0)
        ),
        useBendingCorrection = cms.bool(True)
    )


    process.hltIterL3FromL1MuonPixelTracks = cms.EDProducer("PixelTrackProducer",
        Cleaner = cms.string('hltPixelTracksCleanerBySharedHits'),
        Filter = cms.InputTag("hltIterL3MuonPixelTracksFilter"),
        Fitter = cms.InputTag("hltIterL3MuonPixelTracksFitter"),
        SeedingHitSets = cms.InputTag("hltIterL3FromL1MuonPixelTracksHitQuadruplets"),
        passLabel = cms.string('')
    )


    process.hltIterL3FromL1MuonPixelVertices = cms.EDProducer("PixelVertexProducer",
        Finder = cms.string('DivisiveVertexFinder'),
        Method2 = cms.bool(True),
        NTrkMin = cms.int32(2),
        PVcomparer = cms.PSet(
            refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
        ),
        PtMin = cms.double(1.0),
        TrackCollection = cms.InputTag("hltIterL3MuonPixelTracks"),
        UseError = cms.bool(True),
        Verbosity = cms.int32(0),
        WtAverage = cms.bool(True),
        ZOffset = cms.double(5.0),
        ZSeparation = cms.double(0.05),
        beamSpot = cms.InputTag("hltOnlineBeamSpot")
    )


    process.hltIterL3FromL1MuonTrimmedPixelVertices = cms.EDProducer("PixelVertexCollectionTrimmer",
        PVcomparer = cms.PSet(
            refToPSet_ = cms.string('hltPhase2PSetPvClusterComparerForIT')
        ),
        fractionSumPt2 = cms.double(0.3),
        maxVtx = cms.uint32(100),
        minSumPt2 = cms.double(0.0),
        src = cms.InputTag("hltIterL3FromL1MuonPixelVertices")
    )


    #### Iter0 L1seeded
    process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks = cms.EDProducer("SeedGeneratorFromProtoTracksEDProducer",
        InputCollection = cms.InputTag("hltIterL3FromL1MuonPixelTracks"),
        InputVertexCollection = cms.InputTag("hltIterL3FromL1MuonTrimmedPixelVertices"),
        SeedCreatorPSet = cms.PSet(
            refToPSet_ = cms.string('hltPhase2SeedFromProtoTracks')
        ),
        TTRHBuilder = cms.string('WithTrackAngle'),
        originHalfLength = cms.double(0.3),
        originRadius = cms.double(0.1),
        useEventsWithNoVertex = cms.bool(True),
        usePV = cms.bool(False),
        useProtoTrackKinematics = cms.bool(False)
    )


    process.hltIter0IterL3FromL1MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('none'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string('GroupedCkfTrajectoryBuilder'),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT')
        ),
        TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(True),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        src = cms.InputTag("hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks"),
        useHitsSplitting = cms.bool(True)
    )


    process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('hltIter0'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltSiStripClusters"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),    
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIter0IterL3FromL1MuonCkfTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )


    process.hltIter0IterL3FromL1MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
                d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
                dr_exp = cms.vint32(4, 4, 2147483647),
                dr_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dr_par2 = cms.vdouble(0.3, 0.3, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 2147483647),
                dz_par1 = cms.vdouble(0.4, 0.4, 3.40282346639e+38),
                dz_par2 = cms.vdouble(0.35, 0.35, 3.40282346639e+38)
            ),
            maxChi2 = cms.vdouble(3.40282346639e+38, 3.40282346639e+38, 3.40282346639e+38),
            maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
            maxLostLayers = cms.vint32(1, 1, 1),
            min3DLayers = cms.vint32(0, 3, 4),
            minLayers = cms.vint32(3, 3, 4),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 3, 4)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracks"),
        vertices = cms.InputTag("hltIterL3FromL1MuonTrimmedPixelVertices")
    )


    process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIter0IterL3FromL1MuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIter0IterL3FromL1MuonCtfWithMaterialTracks")
    )


    process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon = cms.Sequence(
        process.hltIter0IterL3FromL1MuonPixelSeedsFromPixelTracks+
        process.hltIter0IterL3FromL1MuonCkfTrackCandidates+
        process.hltIter0IterL3FromL1MuonCtfWithMaterialTracks+
        process.hltIter0IterL3FromL1MuonTrackCutClassifier+
        process.hltIter0IterL3FromL1MuonTrackSelectionHighPurity)


    #### iter2 L1seeded
    process.hltIter2IterL3FromL1MuonCkfTrackCandidates = cms.EDProducer("CkfTrackCandidateMaker",
        MeasurementTrackerEvent = cms.InputTag("hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
        NavigationSchool = cms.string('SimpleNavigationSchool'),
        RedundantSeedCleaner = cms.string('CachingSeedCleanerBySharedInput'),
        SimpleMagneticField = cms.string('ParabolicMf'),
        TrajectoryBuilder = cms.string(''),
        TrajectoryBuilderPSet = cms.PSet(
            refToPSet_ = cms.string('HLTIter2IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT')
        ),
        TrajectoryCleaner = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        TransientInitialStateEstimatorParameters = cms.PSet(
            numberMeasurementsForFit = cms.int32(4),
            propagatorAlongTISE = cms.string('PropagatorWithMaterialParabolicMf'),
            propagatorOppositeTISE = cms.string('PropagatorWithMaterialParabolicMfOpposite')
        ),
        cleanTrajectoryAfterInOut = cms.bool(False),
        doSeedingRegionRebuilding = cms.bool(False),
        maxNSeeds = cms.uint32(100000),
        maxSeedsBeforeCleaning = cms.uint32(1000),
        src = cms.InputTag("hltIter2IterL3FromL1MuonPixelSeeds"),
        useHitsSplitting = cms.bool(False)
    )


    process.hltIter2IterL3FromL1MuonClustersRefRemoval = cms.EDProducer("TrackClusterRemoverPhase2",
        TrackQuality = cms.string('highPurity'),
        maxChi2 = cms.double(16.0),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32(0),
        oldClusterRemovalInfo = cms.InputTag(""),
        overrideTrkQuals = cms.InputTag(""),
        phase2pixelClusters = cms.InputTag("hltSiPixelClusters"),
        phase2OTClusters = cms.InputTag("siPhase2Clusters"),
        trackClassifier = cms.InputTag("","QualityMasks"),
        trajectories = cms.InputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity")
    )


    process.hltIter2IterL3FromL1MuonCtfWithMaterialTracks = cms.EDProducer("TrackProducer",
        AlgorithmName = cms.string('hltIter2'),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        GeometricInnerState = cms.bool(True),
        MeasurementTracker = cms.string(''),
        MeasurementTrackerEvent = cms.InputTag("hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent"),
        NavigationSchool = cms.string(''),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        SimpleMagneticField = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        TrajectoryInEvent = cms.bool(False),
        alias = cms.untracked.string('ctfWithMaterialTracks'),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        clusterRemovalInfo = cms.InputTag(""),
        src = cms.InputTag("hltIter2IterL3FromL1MuonCkfTrackCandidates"),
        useHitsSplitting = cms.bool(False),
        useSimpleMF = cms.bool(False)
    )

    process.hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent = cms.EDProducer("MaskedMeasurementTrackerEventProducer",
        OnDemand = cms.bool(False),
        phase2clustersToSkip = cms.InputTag("hltIter2IterL3FromL1MuonClustersRefRemoval"),
        src = cms.InputTag("hltSiStripClusters")
    )

    process.hltIter2IterL3FromL1MuonMerged = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(20.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity", "hltIter2IterL3FromL1MuonTrackSelectionHighPurity"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag("hltIter0IterL3FromL1MuonTrackSelectionHighPurity", "hltIter2IterL3FromL1MuonTrackSelectionHighPurity"),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(False),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )


    process.hltIter2IterL3FromL1MuonPixelClusterCheck = cms.EDProducer("ClusterCheckerEDProducer",
        ClusterCollectionLabel = cms.InputTag("hltSiStripClusters"),
        MaxNumberOfCosmicClusters = cms.uint32(50000),
        MaxNumberOfPixelClusters = cms.uint32(10000),
        PixelClusterCollectionLabel = cms.InputTag("hltSiPixelClusters"),
        cut = cms.string(''),
        doClusterCheck = cms.bool(False),
        silentClusterCheck = cms.untracked.bool(False)
    )


    process.hltIter2IterL3FromL1MuonPixelHitDoublets = cms.EDProducer("HitPairEDProducer",
        clusterCheck = cms.InputTag("hltIter2IterL3FromL1MuonPixelClusterCheck"),
        layerPairs = cms.vuint32(0, 1),
        maxElement = cms.uint32(0),
        produceIntermediateHitDoublets = cms.bool(True),
        produceSeedingHitSets = cms.bool(False),
        seedingLayers = cms.InputTag("hltIter2IterL3FromL1MuonPixelLayerTriplets"),
        trackingRegions = cms.InputTag("hltIterL3FromL1MuonPixelTracksTrackingRegions"),
        trackingRegionsSeedingLayers = cms.InputTag("")
    )


    process.hltIter2IterL3FromL1MuonPixelHitTriplets = cms.EDProducer("CAHitTripletEDProducer",
        CAHardPtCut = cms.double(0.3),
        CAPhiCut = cms.double(0.1),
        CAThetaCut = cms.double(0.015),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        doublets = cms.InputTag("hltIter2IterL3FromL1MuonPixelHitDoublets"),
        extraHitRPhitolerance = cms.double(0.032),
        maxChi2 = cms.PSet(
            enabled = cms.bool(True),
            pt1 = cms.double(0.8),
            pt2 = cms.double(8.0),
            value1 = cms.double(100.0),
            value2 = cms.double(6.0)
        ),
        useBendingCorrection = cms.bool(True)
    )


    process.hltIter2IterL3FromL1MuonPixelLayerTriplets = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltIter2IterL3FromL1MuonClustersRefRemoval"),
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            skipClusters = cms.InputTag("hltIter2IterL3FromL1MuonClustersRefRemoval"),
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3', 
            'BPix2+BPix3+BPix4', 
            'BPix1+BPix3+BPix4', 
            'BPix1+BPix2+BPix4', 
            'BPix2+BPix3+FPix1_pos', 
            'BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos', 
            'BPix1+BPix2+FPix1_neg', 
            'BPix2+FPix1_pos+FPix2_pos', 
            'BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos', 
            'BPix1+FPix1_neg+FPix2_neg', 
            'FPix1_pos+FPix2_pos+FPix3_pos', 
            'FPix1_neg+FPix2_neg+FPix3_neg', 
            'BPix1+BPix3+FPix1_pos', 
            'BPix1+BPix2+FPix2_pos', 
            'BPix1+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix2_neg', 
            'BPix1+FPix2_neg+FPix3_neg', 
            'BPix1+FPix1_neg+FPix3_neg', 
            'BPix1+FPix2_pos+FPix3_pos', 
            'BPix1+FPix1_pos+FPix3_pos'
        )
    )


    process.hltIter2IterL3FromL1MuonPixelSeeds = cms.EDProducer("SeedCreatorFromRegionConsecutiveHitsTripletOnlyEDProducer",
        MinOneOverPtError = cms.double(1.0),
        OriginTransverseErrorMultiplier = cms.double(1.0),
        SeedComparitorPSet = cms.PSet(
            ComponentName = cms.string('none')
        ),
        SeedMomentumForBOFF = cms.double(5.0),
        TTRHBuilder = cms.string('WithTrackAngle'),
        forceKinematicWithRegionDirection = cms.bool(False),
        magneticField = cms.string('ParabolicMf'),
        propagator = cms.string('PropagatorWithMaterialParabolicMf'),
        seedingHitSets = cms.InputTag("hltIter2IterL3FromL1MuonPixelHitTriplets")
    )


    process.hltIter2IterL3FromL1MuonTrackCutClassifier = cms.EDProducer("TrackCutClassifier",
        beamspot = cms.InputTag("hltOnlineBeamSpot"),
        ignoreVertices = cms.bool(False),
        mva = cms.PSet(
            dr_par = cms.PSet(
                d0err = cms.vdouble(0.003, 0.003, 3.40282346639e+38),
                d0err_par = cms.vdouble(0.001, 0.001, 3.40282346639e+38),
                dr_exp = cms.vint32(4, 4, 2147483647),
                dr_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
                dr_par2 = cms.vdouble(3.40282346639e+38, 0.3, 3.40282346639e+38)
            ),
            dz_par = cms.PSet(
                dz_exp = cms.vint32(4, 4, 2147483647),
                dz_par1 = cms.vdouble(3.40282346639e+38, 0.4, 3.40282346639e+38),
                dz_par2 = cms.vdouble(3.40282346639e+38, 0.35, 3.40282346639e+38)
            ),
            maxChi2 = cms.vdouble(9999.0, 25.0, 3.40282346639e+38),
            maxChi2n = cms.vdouble(1.2, 1.0, 0.7),
            maxDr = cms.vdouble(0.5, 0.03, 3.40282346639e+38),
            maxDz = cms.vdouble(0.5, 0.2, 3.40282346639e+38),
            maxDzWrtBS = cms.vdouble(3.40282346639e+38, 24.0, 100.0),
            maxLostLayers = cms.vint32(1, 1, 1),
            min3DLayers = cms.vint32(0, 0, 0),
            minLayers = cms.vint32(3, 3, 3),
            minNVtxTrk = cms.int32(3),
            minNdof = cms.vdouble(1e-05, 1e-05, 1e-05),
            minPixelHits = cms.vint32(0, 0, 0)
        ),
        qualityCuts = cms.vdouble(-0.7, 0.1, 0.7),
        src = cms.InputTag("hltIter2IterL3FromL1MuonCtfWithMaterialTracks"),
        vertices = cms.InputTag("hltIterL3FromL1MuonTrimmedPixelVertices")
    )


    process.hltIter2IterL3FromL1MuonTrackSelectionHighPurity = cms.EDProducer("TrackCollectionFilterCloner",
        copyExtras = cms.untracked.bool(True),
        copyTrajectories = cms.untracked.bool(False),
        minQuality = cms.string('highPurity'),
        originalMVAVals = cms.InputTag("hltIter2IterL3FromL1MuonTrackCutClassifier","MVAValues"),
        originalQualVals = cms.InputTag("hltIter2IterL3FromL1MuonTrackCutClassifier","QualityMasks"),
        originalSource = cms.InputTag("hltIter2IterL3FromL1MuonCtfWithMaterialTracks")
    )


    process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon = cms.Sequence(
        process.hltIter2IterL3FromL1MuonClustersRefRemoval+
        process.hltIter2IterL3FromL1MuonMaskedMeasurementTrackerEvent+
        process.hltIter2IterL3FromL1MuonPixelLayerTriplets+
        process.hltIter2IterL3FromL1MuonPixelClusterCheck+
        process.hltIter2IterL3FromL1MuonPixelHitDoublets+
        process.hltIter2IterL3FromL1MuonPixelHitTriplets+
        process.hltIter2IterL3FromL1MuonPixelSeeds+
        process.hltIter2IterL3FromL1MuonCkfTrackCandidates+
        process.hltIter2IterL3FromL1MuonCtfWithMaterialTracks+
        process.hltIter2IterL3FromL1MuonTrackCutClassifier+
        process.hltIter2IterL3FromL1MuonTrackSelectionHighPurity)

    process.hltIterL3MuonMerged = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(20.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurity", "hltIter2IterL3MuonMerged"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag("hltIterL3OIMuonTrackSelectionHighPurity", "hltIter2IterL3MuonMerged"),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(False),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    process.hltIterL3MuonAndMuonFromL1Merged = cms.EDProducer("TrackListMerger",
        Epsilon = cms.double(-0.001),
        FoundHitBonus = cms.double(5.0),
        LostHitPenalty = cms.double(20.0),
        MaxNormalizedChisq = cms.double(1000.0),
        MinFound = cms.int32(3),
        MinPT = cms.double(0.05),
        ShareFrac = cms.double(0.19),
        TrackProducers = cms.VInputTag("hltIterL3MuonMerged", "hltIter2IterL3FromL1MuonMerged"),
        allowFirstHitShare = cms.bool(True),
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        hasSelector = cms.vint32(0, 0),
        indivShareFrac = cms.vdouble(1.0, 1.0),
        newQuality = cms.string('confirmed'),
        selectedTrackQuals = cms.VInputTag("hltIterL3MuonMerged", "hltIter2IterL3FromL1MuonMerged"),
        setsToMerge = cms.VPSet(cms.PSet(
            pQual = cms.bool(False),
            tLists = cms.vint32(0, 1)
        )),
        trackAlgoPriorityOrder = cms.string('hltESPTrackAlgoPriorityOrder'),
        writeOnlyTrkQuals = cms.bool(False)
    )

    process.hltIterL3GlbMuon = cms.EDProducer("L3MuonProducer",
        L3TrajBuilderParameters = cms.PSet(
            GlbRefitterParameters = cms.PSet(
                CSCRecSegmentLabel = cms.InputTag("hltCscSegments"),
                Chi2CutCSC = cms.double(150.0),
                Chi2CutDT = cms.double(10.0),
                Chi2CutRPC = cms.double(1.0),
                DTRecSegmentLabel = cms.InputTag("hltDt4DSegments"),
                DYTthrs = cms.vint32(30, 15),
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                HitThreshold = cms.int32(1),
                MuonHitsOption = cms.int32(1),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                PropDirForCosmics = cms.bool(False),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitFlag = cms.bool(True),
                RefitRPCHits = cms.bool(True),
                SkipStation = cms.int32(-1),
                TrackerRecHitBuilder = cms.string('WithTrackAngle'),
                TrackerSkipSection = cms.int32(-1),
                TrackerSkipSystem = cms.int32(-1)
            ),
            GlobalMuonTrackMatcher = cms.PSet(
                Chi2Cut_1 = cms.double(50.0),
                Chi2Cut_2 = cms.double(50.0),
                Chi2Cut_3 = cms.double(200.0),
                DeltaDCut_1 = cms.double(40.0),
                DeltaDCut_2 = cms.double(10.0),
                DeltaDCut_3 = cms.double(15.0),
                DeltaRCut_1 = cms.double(0.1),
                DeltaRCut_2 = cms.double(0.2),
                DeltaRCut_3 = cms.double(1.0),
                Eta_threshold = cms.double(1.2),
                LocChi2Cut = cms.double(0.001),
                MinP = cms.double(2.5),
                MinPt = cms.double(1.0),
                Propagator = cms.string('hltESPSmartPropagator'),
                Pt_threshold1 = cms.double(0.0),
                Pt_threshold2 = cms.double(999999999.0),
                Quality_1 = cms.double(20.0),
                Quality_2 = cms.double(15.0),
                Quality_3 = cms.double(7.0)
            ),
            MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
            MuonTrackingRegionBuilder = cms.PSet(
                DeltaEta = cms.double(0.2),
                DeltaPhi = cms.double(0.15),
                DeltaR = cms.double(0.025),
                DeltaZ = cms.double(24.2),
                EtaR_UpperLimit_Par1 = cms.double(0.25),
                EtaR_UpperLimit_Par2 = cms.double(0.15),
                Eta_fixed = cms.bool(True),
                Eta_min = cms.double(0.1),
                MeasurementTrackerName = cms.InputTag("hltESPMeasurementTracker"),
                OnDemand = cms.int32(-1),
                PhiR_UpperLimit_Par1 = cms.double(0.6),
                PhiR_UpperLimit_Par2 = cms.double(0.2),
                Phi_fixed = cms.bool(True),
                Phi_min = cms.double(0.1),
                Pt_fixed = cms.bool(False),
                Pt_min = cms.double(3.0),
                Rescale_Dz = cms.double(4.0),
                Rescale_eta = cms.double(3.0),
                Rescale_phi = cms.double(3.0),
                UseVertex = cms.bool(False),
                Z_fixed = cms.bool(False),
                beamSpot = cms.InputTag("hltOnlineBeamSpot"),
                input = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
                maxRegions = cms.int32(2),
                precise = cms.bool(True),
                vertexCollection = cms.InputTag("pixelVertices")
            ),
            PCut = cms.double(2.5),
            PtCut = cms.double(1.0),
            RefitRPCHits = cms.bool(True),
            ScaleTECxFactor = cms.double(-1.0),
            ScaleTECyFactor = cms.double(-1.0),
            TrackTransformer = cms.PSet(
                DoPredictionsOnly = cms.bool(False),
                Fitter = cms.string('hltESPL3MuKFTrajectoryFitter'),
                MuonRecHitBuilder = cms.string('hltESPMuonTransientTrackingRecHitBuilder'),
                Propagator = cms.string('hltESPSmartPropagatorAny'),
                RefitDirection = cms.string('insideOut'),
                RefitRPCHits = cms.bool(True),
                Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
                TrackerRecHitBuilder = cms.string('WithTrackAngle')
            ),
            TrackerPropagator = cms.string('SteppingHelixPropagatorAny'),
            TrackerRecHitBuilder = cms.string('WithTrackAngle'),
            tkTrajBeamSpot = cms.InputTag("hltOnlineBeamSpot"),
            tkTrajLabel = cms.InputTag("hltIterL3MuonAndMuonFromL1Merged"),
            tkTrajMaxChi2 = cms.double(9999.0),
            tkTrajMaxDXYBeamSpot = cms.double(9999.0),
            tkTrajUseVertex = cms.bool(False),
            tkTrajVertex = cms.InputTag("Notused")
        ),
        MuonCollectionLabel = cms.InputTag("hltL2Muons","UpdatedAtVtx"),
        ServiceParameters = cms.PSet(
            Propagators = cms.untracked.vstring(
                'hltESPSmartPropagatorAny', 
                'SteppingHelixPropagatorAny', 
                'hltESPSmartPropagator', 
                'hltESPSteppingHelixPropagatorOpposite'
            ),
            RPCLayers = cms.bool(True),
            UseMuonNavigation = cms.untracked.bool(True)
        ),
        TrackLoaderParameters = cms.PSet(
            DoSmoothing = cms.bool(True),
            MuonSeededTracksInstance = cms.untracked.string('L2Seeded'),
            MuonUpdatorAtVertexParameters = cms.PSet(
                BeamSpotPositionErrors = cms.vdouble(0.1, 0.1, 5.3),
                MaxChi2 = cms.double(1000000.0),
                Propagator = cms.string('hltESPSteppingHelixPropagatorOpposite')
            ),
            PutTkTrackIntoEvent = cms.untracked.bool(False),
            SmoothTkTrack = cms.untracked.bool(False),
            Smoother = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
            TTRHBuilder = cms.string('WithTrackAngle'),
            VertexConstraint = cms.bool(False),
            beamSpot = cms.InputTag("hltOnlineBeamSpot")
        )
    )

    process.hltIterL3MuonsNoID = cms.EDProducer("MuonIdProducer",
        CaloExtractorPSet = cms.PSet(
            CenterConeOnCalIntersection = cms.bool(False),
            ComponentName = cms.string('CaloExtractorByAssociator'),
            DR_Max = cms.double(1.0),
            DR_Veto_E = cms.double(0.07),
            DR_Veto_H = cms.double(0.1),
            DR_Veto_HO = cms.double(0.1),
            DepositInstanceLabels = cms.vstring(
                'ecal', 
                'hcal', 
                'ho'
            ),
            DepositLabel = cms.untracked.string('Cal'),
            NoiseTow_EB = cms.double(0.04),
            NoiseTow_EE = cms.double(0.15),
            Noise_EB = cms.double(0.025),
            Noise_EE = cms.double(0.1),
            Noise_HB = cms.double(0.2),
            Noise_HE = cms.double(0.2),
            Noise_HO = cms.double(0.2),
            PrintTimeReport = cms.untracked.bool(False),
            PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(False),
                UseMuonNavigation = cms.untracked.bool(False)
            ),
            Threshold_E = cms.double(0.2),
            Threshold_H = cms.double(0.5),
            Threshold_HO = cms.double(0.5),
            TrackAssociatorParameters = cms.PSet(
                CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
                CaloTowerCollectionLabel = cms.InputTag("Notused"),
                DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
                EBRecHitCollectionLabel = cms.InputTag("Notused"),
                EERecHitCollectionLabel = cms.InputTag("Notused"),
                HBHERecHitCollectionLabel = cms.InputTag("Notused"),
                HORecHitCollectionLabel = cms.InputTag("Notused"),
                accountForTrajectoryChangeCalo = cms.bool(False),
                dREcal = cms.double(1.0),
                dREcalPreselection = cms.double(1.0),
                dRHcal = cms.double(1.0),
                dRHcalPreselection = cms.double(1.0),
                dRMuon = cms.double(9999.0),
                dRMuonPreselection = cms.double(0.2),
                dRPreshowerPreselection = cms.double(0.2),
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                propagateAllDirections = cms.bool(True),
                trajectoryUncertaintyTolerance = cms.double(-1.0),
                truthMatch = cms.bool(False),
                useCalo = cms.bool(True),
                useEcal = cms.bool(False),
                useHO = cms.bool(False),
                useHcal = cms.bool(False),
                useMuon = cms.bool(False),
                usePreshower = cms.bool(False)
            ),
            UseRecHitsFlag = cms.bool(False)
        ),
        JetExtractorPSet = cms.PSet(
            ComponentName = cms.string('JetExtractor'),
            DR_Max = cms.double(1.0),
            DR_Veto = cms.double(0.1),
            ExcludeMuonVeto = cms.bool(True),
            JetCollectionLabel = cms.InputTag("Notused"),
            PrintTimeReport = cms.untracked.bool(False),
            PropagatorName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
            ServiceParameters = cms.PSet(
                Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                RPCLayers = cms.bool(False),
                UseMuonNavigation = cms.untracked.bool(False)
            ),
            Threshold = cms.double(5.0),
            TrackAssociatorParameters = cms.PSet(
                CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
                CaloTowerCollectionLabel = cms.InputTag("Notused"),
                DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
                EBRecHitCollectionLabel = cms.InputTag("Notused"),
                EERecHitCollectionLabel = cms.InputTag("Notused"),
                HBHERecHitCollectionLabel = cms.InputTag("Notused"),
                HORecHitCollectionLabel = cms.InputTag("Notused"),
                accountForTrajectoryChangeCalo = cms.bool(False),
                dREcal = cms.double(0.5),
                dREcalPreselection = cms.double(0.5),
                dRHcal = cms.double(0.5),
                dRHcalPreselection = cms.double(0.5),
                dRMuon = cms.double(9999.0),
                dRMuonPreselection = cms.double(0.2),
                dRPreshowerPreselection = cms.double(0.2),
                muonMaxDistanceSigmaX = cms.double(0.0),
                muonMaxDistanceSigmaY = cms.double(0.0),
                muonMaxDistanceX = cms.double(5.0),
                muonMaxDistanceY = cms.double(5.0),
                propagateAllDirections = cms.bool(True),
                trajectoryUncertaintyTolerance = cms.double(-1.0),
                truthMatch = cms.bool(False),
                useCalo = cms.bool(True),
                useEcal = cms.bool(False),
                useHO = cms.bool(False),
                useHcal = cms.bool(False),
                useMuon = cms.bool(False),
                usePreshower = cms.bool(False)
            )
        ),
        MuonCaloCompatibility = cms.PSet(
            MuonTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_muons_lowPt_3_1_norm.root'),
            PionTemplateFileName = cms.FileInPath('RecoMuon/MuonIdentification/data/MuID_templates_pions_lowPt_3_1_norm.root'),
            allSiPMHO = cms.bool(False),
            delta_eta = cms.double(0.02),
            delta_phi = cms.double(0.02)
        ),
        TimingFillerParameters = cms.PSet(
            CSCTimingParameters = cms.PSet(
                CSCStripError = cms.double(7.0),
                CSCStripTimeOffset = cms.double(0.0),
                CSCTimeOffset = cms.double(0.0),
                CSCWireError = cms.double(8.6),
                CSCWireTimeOffset = cms.double(0.0),
                CSCsegments = cms.InputTag("hltCscSegments"),
                MatchParameters = cms.PSet(
                    CSCsegments = cms.InputTag("hltCscSegments"),
                    DTradius = cms.double(0.01),
                    DTsegments = cms.InputTag("hltDt4DSegments"),
                    TightMatchCSC = cms.bool(True),
                    TightMatchDT = cms.bool(False)
                ),
                PruneCut = cms.double(100.0),
                ServiceParameters = cms.PSet(
                    Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                    RPCLayers = cms.bool(True)
                ),
                UseStripTime = cms.bool(True),
                UseWireTime = cms.bool(True),
                debug = cms.bool(False)
            ),
            DTTimingParameters = cms.PSet(
                DTTimeOffset = cms.double(2.7),
                DTsegments = cms.InputTag("hltDt4DSegments"),
                DoWireCorr = cms.bool(False),
                DropTheta = cms.bool(True),
                HitError = cms.double(6.0),
                HitsMin = cms.int32(5),
                MatchParameters = cms.PSet(
                    CSCsegments = cms.InputTag("hltCscSegments"),
                    DTradius = cms.double(0.01),
                    DTsegments = cms.InputTag("hltDt4DSegments"),
                    TightMatchCSC = cms.bool(True),
                    TightMatchDT = cms.bool(False)
                ),
                PruneCut = cms.double(10000.0),
                RequireBothProjections = cms.bool(False),
                ServiceParameters = cms.PSet(
                    Propagators = cms.untracked.vstring('hltESPFastSteppingHelixPropagatorAny'),
                    RPCLayers = cms.bool(True)
                ),
                UseSegmentT0 = cms.bool(False),
                debug = cms.bool(False)
            ),
            EcalEnergyCut = cms.double(0.4),
            ErrorCSC = cms.double(7.4),
            ErrorDT = cms.double(6.0),
            ErrorEB = cms.double(2.085),
            ErrorEE = cms.double(6.95),
            UseCSC = cms.bool(True),
            UseDT = cms.bool(True),
            UseECAL = cms.bool(True)
        ),
        TrackAssociatorParameters = cms.PSet(
            CSCSegmentCollectionLabel = cms.InputTag("hltCscSegments"),
            CaloTowerCollectionLabel = cms.InputTag("Notused"),
            DTRecSegment4DCollectionLabel = cms.InputTag("hltDt4DSegments"),
            EBRecHitCollectionLabel = cms.InputTag("Notused"),
            EERecHitCollectionLabel = cms.InputTag("Notused"),
            HBHERecHitCollectionLabel = cms.InputTag("Notused"),
            HORecHitCollectionLabel = cms.InputTag("Notused"),
            accountForTrajectoryChangeCalo = cms.bool(False),
            dREcal = cms.double(9999.0),
            dREcalPreselection = cms.double(0.05),
            dRHcal = cms.double(9999.0),
            dRHcalPreselection = cms.double(0.2),
            dRMuon = cms.double(9999.0),
            dRMuonPreselection = cms.double(0.2),
            dRPreshowerPreselection = cms.double(0.2),
            muonMaxDistanceSigmaX = cms.double(0.0),
            muonMaxDistanceSigmaY = cms.double(0.0),
            muonMaxDistanceX = cms.double(5.0),
            muonMaxDistanceY = cms.double(5.0),
            propagateAllDirections = cms.bool(True),
            trajectoryUncertaintyTolerance = cms.double(-1.0),
            truthMatch = cms.bool(False),
            useCalo = cms.bool(False),
            useEcal = cms.bool(False),
            useHO = cms.bool(False),
            useHcal = cms.bool(False),
            useMuon = cms.bool(True),
            usePreshower = cms.bool(False)
        ),
        TrackExtractorPSet = cms.PSet(
            BeamSpotLabel = cms.InputTag("hltOnlineBeamSpot"),
            BeamlineOption = cms.string('BeamSpotFromEvent'),
            Chi2Ndof_Max = cms.double(1e+64),
            Chi2Prob_Min = cms.double(-1.0),
            ComponentName = cms.string('TrackExtractor'),
            DR_Max = cms.double(1.0),
            DR_Veto = cms.double(0.01),
            Diff_r = cms.double(0.1),
            Diff_z = cms.double(0.2),
            NHits_Min = cms.uint32(0),
            Pt_Min = cms.double(-1.0),
            inputTrackCollection = cms.InputTag("hltIter2IterL3FromL1MuonMerged")
        ),
        TrackerKinkFinderParameters = cms.PSet(
            diagonalOnly = cms.bool(False),
            usePosition = cms.bool(False)
        ),
        addExtraSoftMuons = cms.bool(False),
        arbitrateTrackerMuons = cms.bool(True),
        arbitrationCleanerOptions = cms.PSet(
            ClusterDPhi = cms.double(0.6),
            ClusterDTheta = cms.double(0.02),
            Clustering = cms.bool(True),
            ME1a = cms.bool(True),
            Overlap = cms.bool(True),
            OverlapDPhi = cms.double(0.0786),
            OverlapDTheta = cms.double(0.02)
        ),
        debugWithTruthMatching = cms.bool(False),
        ecalDepositName = cms.string('ecal'),
        fillCaloCompatibility = cms.bool(False),
        fillEnergy = cms.bool(False),
        fillGlobalTrackQuality = cms.bool(False),
        fillGlobalTrackRefits = cms.bool(False),
        fillIsolation = cms.bool(False),
        fillMatching = cms.bool(True),
        fillTrackerKink = cms.bool(False),
        globalTrackQualityInputTag = cms.InputTag("glbTrackQual"),
        hcalDepositName = cms.string('hcal'),
        hoDepositName = cms.string('ho'),
        inputCollectionLabels = cms.VInputTag("hltIterL3MuonAndMuonFromL1Merged", "hltIterL3GlbMuon", "hltL2Muons:UpdatedAtVtx"),
        inputCollectionTypes = cms.vstring(
            'inner tracks', 
            'links', 
            'outer tracks'
        ),
        jetDepositName = cms.string('jets'),
        maxAbsDx = cms.double(3.0),
        maxAbsDy = cms.double(9999.0),
        maxAbsEta = cms.double(3.0),
        maxAbsPullX = cms.double(4.0),
        maxAbsPullY = cms.double(9999.0),
        minCaloCompatibility = cms.double(0.6),
        minNumberOfMatches = cms.int32(1),
        minP = cms.double(0.0),
        minPCaloMuon = cms.double(1000000000.0),
        minPt = cms.double(2.0),
        ptThresholdToFillCandidateP4WithGlobalFit = cms.double(200.0),
        runArbitrationCleaner = cms.bool(False),
        sigmaThresholdToFillCandidateP4WithGlobalFit = cms.double(2.0),
        trackDepositName = cms.string('tracker'),
        writeIsoDeposits = cms.bool(False)
    )

    process.hltIterL3Muons = cms.EDProducer("MuonIDFilterProducerForHLT",
        allowedTypeMask = cms.uint32(0),
        applyTriggerIdLoose = cms.bool(True),
        inputMuonCollection = cms.InputTag("hltIterL3MuonsNoID"),
        maxNormalizedChi2 = cms.double(9999.0),
        minNMuonHits = cms.int32(0),
        minNMuonStations = cms.int32(0),
        minNTrkLayers = cms.int32(0),
        minPixHits = cms.int32(0),
        minPixLayer = cms.int32(0),
        minPt = cms.double(0.0),
        minTrkHits = cms.int32(0),
        requiredTypeMask = cms.uint32(0),
        typeMuon = cms.uint32(0)
    )

    process.hltL3MuonsIterL3Links = cms.EDProducer("MuonLinksProducer",
        inputCollection = cms.InputTag("hltIterL3Muons")
    )

    process.hltIterL3MuonTracks = cms.EDProducer("HLTMuonTrackSelector",
        copyExtras = cms.untracked.bool(True),
        copyMVA = cms.bool(False),
        copyTrajectories = cms.untracked.bool(False),
        muon = cms.InputTag("hltIterL3Muons"),
        originalMVAVals = cms.InputTag("none"),
        track = cms.InputTag("hltIterL3MuonAndMuonFromL1Merged")
    )


    process.HLTIterL3MuonRecoPixelTracksSequence = cms.Sequence(process.hltIterL3MuonPixelTracksFilter+
                                                                process.hltIterL3MuonPixelTracksFitter+
                                                                process.hltIterL3MuonPixelTracksTrackingRegions+
                                                                process.hltIterL3MuonPixelLayerQuadruplets+
                                                                process.hltIterL3MuonPixelTracksHitDoublets+
                                                                process.hltIterL3MuonPixelTracksHitQuadruplets+
                                                                process.hltIterL3MuonPixelTracks)


    process.HLTIterL3MuonRecopixelvertexingSequence = cms.Sequence(process.HLTIterL3MuonRecoPixelTracksSequence+
                                                                   process.hltIterL3MuonPixelVertices+
                                                                   process.hltIterL3MuonTrimmedPixelVertices)

    process.HLTIterativeTrackingIter02ForIterL3Muon = cms.Sequence(process.HLTIterativeTrackingIteration0ForIterL3Muon+
                                                                   process.HLTIterativeTrackingIteration2ForIterL3Muon+
                                                                   process.hltIter2IterL3MuonMerged)


    process.HLTIterL3IOmuonTkCandidateSequence = cms.Sequence(process.HLTIterL3MuonRecopixelvertexingSequence+
                                                              process.HLTIterativeTrackingIter02ForIterL3Muon+
                                                              process.hltL3MuonsIterL3IO)


    process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence = cms.Sequence(process.HLTIterL3OImuonTkCandidateSequence+
                                                                         process.hltIterL3OIL3MuonsLinksCombination+
                                                                         process.hltIterL3OIL3Muons+
                                                                         process.hltIterL3OIL3MuonCandidates+
                                                                         process.hltL2SelectorForL3IO+
                                                                         process.HLTIterL3IOmuonTkCandidateSequence+
                                                                         process.hltIterL3MuonsFromL2LinksCombination)


    process.HLTRecoPixelTracksSequenceForIterL3FromL1Muon = cms.Sequence(process.hltIterL3FromL1MuonPixelTracksTrackingRegions+
                                                                         process.hltIterL3FromL1MuonPixelLayerQuadruplets+
                                                                         process.hltIterL3FromL1MuonPixelTracksHitDoublets+
                                                                         process.hltIterL3FromL1MuonPixelTracksHitQuadruplets+
                                                                         process.hltIterL3FromL1MuonPixelTracks)

    process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon = cms.Sequence(process.HLTRecoPixelTracksSequenceForIterL3FromL1Muon+
                                                                            process.hltIterL3FromL1MuonPixelVertices+
                                                                            process.hltIterL3FromL1MuonTrimmedPixelVertices)

    process.HLTIterativeTrackingIter02ForIterL3FromL1Muon = cms.Sequence(process.HLTIterativeTrackingIteration0ForIterL3FromL1Muon+
                                                                         process.HLTIterativeTrackingIteration2ForIterL3FromL1Muon+
                                                                         process.hltIter2IterL3FromL1MuonMerged)

    process.HLTIterL3IOmuonFromL1TkCandidateSequence = cms.Sequence(process.HLTRecopixelvertexingSequenceForIterL3FromL1Muon+
                                                                    process.HLTIterativeTrackingIter02ForIterL3FromL1Muon)

    process.HLTIterL3muonTkCandidateSequence = cms.Sequence(process.HLTDoLocalPixelSequence+
                                                            process.HLTDoLocalStripSequence+
                                                            process.HLTIterL3OIAndIOFromL2muonTkCandidateSequence+
                                                            #process.hltL1MuonsPt0+###for Mu50
                                                            process.hltIterL3MuonL1MuonNoL2Selector + 
                                                            process.HLTIterL3IOmuonFromL1TkCandidateSequence
                                                            )

    process.HLTL3muonrecoNocandSequence = cms.Sequence(process.HLTIterL3muonTkCandidateSequence+
                                                       process.hltIterL3MuonMerged+
                                                       process.hltIterL3MuonAndMuonFromL1Merged+
                                                       process.hltIterL3GlbMuon+
                                                       process.hltIterL3MuonsNoID+
                                                       process.hltIterL3Muons+
                                                       process.hltL3MuonsIterL3Links+
                                                       process.hltIterL3MuonTracks)


    process.hltIterL3MuonCandidates = cms.EDProducer("L3MuonCandidateProducerFromMuons",
                                                     InputObjects = cms.InputTag("hltIterL3Muons")
                                                     )

    process.HLTL3muonrecoSequence = cms.Sequence(process.HLTL3muonrecoNocandSequence+
                                                 process.hltIterL3MuonCandidates
                                                 )


    process.hltBoolEnd = cms.EDFilter("HLTBool",
        result = cms.bool(True)
    )


    process.HLTEndSequence = cms.Sequence(process.hltBoolEnd)



    ######################################
    ### process to define the Mu50 filters
    ######################################
    # process.hltL1sSingleMu22or25 = cms.EDFilter("HLTL1TSeed",
    #     L1EGammaInputTag = cms.InputTag("hltGtStage2Digis","EGamma"),
    #     L1EtSumInputTag = cms.InputTag("hltGtStage2Digis","EtSum"),
    #     L1GlobalInputTag = cms.InputTag("hltGtStage2Digis"),
    #     L1JetInputTag = cms.InputTag("hltGtStage2Digis","Jet"),
    #     L1MuonInputTag = cms.InputTag("hltGtStage2Digis","Muon"),
    #     L1ObjectMapInputTag = cms.InputTag("hltGtStage2ObjectMap"),
    #     L1SeedsLogicalExpression = cms.string('L1_SingleMu22 OR L1_SingleMu25'),
    #     L1TauInputTag = cms.InputTag("hltGtStage2Digis","Tau"),
    #     saveTags = cms.bool(True)
    # )

    # process.hltPreMu50 = cms.EDFilter("HLTPrescaler",
    #     L1GtReadoutRecordTag = cms.InputTag("hltGtStage2Digis"),
    #     offset = cms.uint32(0)
    # )

    # process.hltL1fL1sMu22or25L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
    #     CandTag = cms.InputTag("hltGtStage2Digis","Muon"),
    #     CentralBxOnly = cms.bool(True),
    #     MaxEta = cms.double(2.5),
    #     MinN = cms.int32(1),
    #     MinPt = cms.double(0.0),
    #     PreviousCandTag = cms.InputTag("hltL1sSingleMu22or25"),
    #     SelectQualities = cms.vint32(),
    #     saveTags = cms.bool(True)
    # )

    process.hltL2fL1sMu22or25L1f0L2Filtered10Q = cms.EDFilter("HLTMuonL2FromL1TPreFilter",
        AbsEtaBins = cms.vdouble(0.0),
        BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
        CandTag = cms.InputTag("hltL2MuonCandidates"),
        CutOnChambers = cms.bool(False),
        MatchToPreviousCand = cms.bool(True),
        MaxDr = cms.double(9999.0),
        MaxDz = cms.double(9999.0),
        MaxEta = cms.double(2.5),
        MinDr = cms.double(-1.0),
        MinDxySig = cms.double(-1.0),
        MinN = cms.int32(0),
        MinNchambers = cms.vint32(0),
        MinNhits = cms.vint32(0),
        MinNstations = cms.vint32(0),
        MinPt = cms.double(0.0),
        NSigmaPt = cms.double(0.0),
        PreviousCandTag = cms.InputTag("hltL1fL1sMu22or25L1Filtered0"),
        SeedMapTag = cms.InputTag("hltL2Muons"),
        saveTags = cms.bool(True)
    )

    process.hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q = cms.EDFilter("HLTMuonL3PreFilter",
                                                                    BeamSpotTag = cms.InputTag("hltOnlineBeamSpot"),
                                                                    CandTag = cms.InputTag("hltIterL3MuonCandidates"),
                                                                    InputLinks = cms.InputTag("hltL3MuonsIterL3Links"),
                                                                    L1CandTag = cms.InputTag("hltL1fForIterL3L1fL1sMu22or25L1Filtered0"),
                                                                    L1MatchingdR = cms.double(0.3),
                                                                    MatchToPreviousCand = cms.bool(True),
                                                                    MaxDXYBeamSpot = cms.double(9999.0),
                                                                    MaxDr = cms.double(2.0),
                                                                    MaxDz = cms.double(9999.0),
                                                                    MaxEta = cms.double(1e+99),
                                                                    MaxNormalizedChi2 = cms.double(9999.0),
                                                                    MaxNormalizedChi2_L3FromL1 = cms.double(1e+99),
                                                                    MaxPtDifference = cms.double(9999.0),
                                                                    MinDXYBeamSpot = cms.double(-1.0),
                                                                    MinDr = cms.double(-1.0),
                                                                    MinDxySig = cms.double(-1.0),
                                                                    MinN = cms.int32(1),
                                                                    MinNhits = cms.int32(0),
                                                                    MinNmuonHits = cms.int32(0),
                                                                    MinPt = cms.double(50.0),
                                                                    MinTrackPt = cms.double(0.0),
                                                                    NSigmaPt = cms.double(0.0),
                                                                    PreviousCandTag = cms.InputTag("hltL2fL1sMu22or25L1f0L2Filtered10Q"),
                                                                    allowedTypeMask = cms.uint32(255),
                                                                    inputMuonCollection = cms.InputTag("hltIterL3Muons"),
                                                                    minMuonHits = cms.int32(-1),
                                                                    minMuonStations = cms.int32(2),
                                                                    minTrkHits = cms.int32(-1),
                                                                    requiredTypeMask = cms.uint32(0),
                                                                    saveTags = cms.bool(True),
                                                                    trkMuonId = cms.uint32(0)
                                                                    )


    # process.hltL1MuonsPt0 = cms.EDProducer("HLTL1TMuonSelector",
    #     CentralBxOnly = cms.bool(True),
    #     InputObjects = cms.InputTag("hltGtStage2Digis","Muon"),
    #     L1MaxEta = cms.double(5.0),
    #     L1MinPt = cms.double(-1.0),
    #     L1MinQuality = cms.uint32(7)
    # )

    process.hltL1fForIterL3L1fL1sMu22or25L1Filtered0 = cms.EDFilter("HLTMuonL1TFilter",
        CandTag = cms.InputTag("hltL1MuonsPt0"),
        CentralBxOnly = cms.bool(True),
        MaxEta = cms.double(2.5),
        MinN = cms.int32(1),
        MinPt = cms.double(0.0),
        PreviousCandTag = cms.InputTag("hltL1fL1sMu22or25L1Filtered0"),
        SelectQualities = cms.vint32(),
        saveTags = cms.bool(True)
    )


    #########################################
    ### HLT_Mu50 sequence
    #########################################
    process.HLT_Mu50_v13 = cms.Path(
      process.HLTBeginSequence + 
      # cms.ignore(process.hltL1sSingleMu22or25)+

      # process.hltPreMu50+
      # cms.ignore(process.hltL1fL1sMu22or25L1Filtered0)+
      
      process.HLTL2muonrecoSequence+
      # cms.ignore(process.hltL1MuonsPt0)+
      # cms.ignore(process.hltL2fL1sMu22or25L1f0L2Filtered10Q)+
      
      process.HLTL3muonrecoSequence+
      # cms.ignore(process.hltL1fForIterL3L1fL1sMu22or25L1Filtered0)+
      
      # cms.ignore(process.hltL3fL1sMu22Or25L1f0L2f10QL3Filtered50Q)+
      process.HLTEndSequence
    )


    #########################################
    ### process to define the IsoMu24 filters
    #########################################
    # process.hltL1sSingleMu22 = cms.EDFilter( "HLTL1TSeed",
    #     L1SeedsLogicalExpression = cms.string( "L1_SingleMu22" ),
    #     L1EGammaInputTag = cms.InputTag( 'hltGtStage2Digis','EGamma' ),
    #     L1JetInputTag = cms.InputTag( 'hltGtStage2Digis','Jet' ),
    #     saveTags = cms.bool( True ),
    #     L1ObjectMapInputTag = cms.InputTag( "hltGtStage2ObjectMap" ),
    #     L1EtSumInputTag = cms.InputTag( 'hltGtStage2Digis','EtSum' ),
    #     L1TauInputTag = cms.InputTag( 'hltGtStage2Digis','Tau' ),
    #     L1MuonInputTag = cms.InputTag( 'hltGtStage2Digis','Muon' ),
    #     L1GlobalInputTag = cms.InputTag( "hltGtStage2Digis" )
    # )
    # process.hltPreIsoMu24 = cms.EDFilter( "HLTPrescaler",
    #     L1GtReadoutRecordTag = cms.InputTag( "hltGtStage2Digis" ),
    #     offset = cms.uint32( 0 )
    # )
    # process.hltL1fL1sMu22L1Filtered0 = cms.EDFilter( "HLTMuonL1TFilter",
    #     saveTags = cms.bool( True ),
    #     PreviousCandTag = cms.InputTag( "hltL1sSingleMu22" ),
    #     MinPt = cms.double( 0.0 ),
    #     MinN = cms.int32( 1 ),
    #     MaxEta = cms.double( 2.5 ),
    #     CentralBxOnly = cms.bool( True ),
    #     SelectQualities = cms.vint32(  ),
    #     CandTag = cms.InputTag( 'hltGtStage2Digis','Muon' )
    # )

    ##############
    #PreviuosCand# contains L1filter seed
    process.hltL2fL1sSingleMu22L1f0L2Filtered10Q = cms.EDFilter( "HLTMuonL2FromL1TPreFilter",
        saveTags = cms.bool( True ),
        MaxDr = cms.double( 9999.0 ),
        CutOnChambers = cms.bool( False ),
        PreviousCandTag = cms.InputTag( "hltL1fL1sMu22L1Filtered0" ),
        MinPt = cms.double( 0.0 ),
        MinN = cms.int32( 0 ),
        SeedMapTag = cms.InputTag( "hltL2Muons" ),
        MaxEta = cms.double( 2.5 ),
        MinNhits = cms.vint32( 0 ),
        MinDxySig = cms.double( -1.0 ),
        MinNchambers = cms.vint32( 0 ),
        AbsEtaBins = cms.vdouble( 0.0 ),
        MaxDz = cms.double( 9999.0 ),
        MatchToPreviousCand = cms.bool( False ),
        CandTag = cms.InputTag( "hltL2MuonCandidates" ),
        BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
        MinDr = cms.double( -1.0 ),
        NSigmaPt = cms.double( 0.0 ),
        MinNstations = cms.vint32( 0 )
    )
    process.hltL1fForIterL3L1fL1sMu22L1Filtered0 = cms.EDFilter( "HLTMuonL1TFilter",
        saveTags = cms.bool( True ),
        PreviousCandTag = cms.InputTag( "hltL1fL1sMu22L1Filtered0" ),
        MinPt = cms.double( 0.0 ),
        MinN = cms.int32( 1 ),
        MaxEta = cms.double( 2.5 ),
        CentralBxOnly = cms.bool( True ),
        SelectQualities = cms.vint32(  ),
        CandTag = cms.InputTag( "hltIterL3MuonL1MuonNoL2Selector" )
    )

    process.hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q = cms.EDFilter( "HLTMuonL3PreFilter",
        MaxNormalizedChi2 = cms.double( 9999.0 ),
        saveTags = cms.bool( True ),
        MaxDXYBeamSpot = cms.double( 9999.0 ),
        MinDxySig = cms.double( -1.0 ),
        MatchToPreviousCand = cms.bool( True ),
        MaxPtDifference = cms.double( 9999.0 ),
        MaxDr = cms.double( 2.0 ),
        L1CandTag = cms.InputTag( "hltL1fForIterL3L1fL1sMu22L1Filtered0" ),
        MaxNormalizedChi2_L3FromL1 = cms.double( 1.0E99 ),
        inputMuonCollection = cms.InputTag( "hltIterL3Muons" ),
        InputLinks = cms.InputTag( "hltL3MuonsIterL3Links" ),
        PreviousCandTag = cms.InputTag( "hltL2fL1sSingleMu22L1f0L2Filtered10Q" ),
        MaxEta = cms.double( 1.0E99 ),
        trkMuonId = cms.uint32( 0 ),
        MinDr = cms.double( -1.0 ),
        BeamSpotTag = cms.InputTag( "hltOnlineBeamSpot" ),
        MinNmuonHits = cms.int32( 0 ),
        MinN = cms.int32( 1 ),
        MinTrackPt = cms.double( 0.0 ),
        requiredTypeMask = cms.uint32( 0 ),
        MaxDz = cms.double( 9999.0 ),
        minMuonHits = cms.int32( -1 ),
        minTrkHits = cms.int32( -1 ),
        MinDXYBeamSpot = cms.double( -1.0 ),
        allowedTypeMask = cms.uint32( 255 ),
        MinPt = cms.double( 24.0 ),
        MinNhits = cms.int32( 0 ),
        minMuonStations = cms.int32( 2 ),
        NSigmaPt = cms.double( 0.0 ),
        CandTag = cms.InputTag( "hltIterL3MuonCandidates" ),
        L1MatchingdR = cms.double( 0.3 )
    )



    ##########################################
    ### processes for PF (ECAL HCAL) Isolation
    ##########################################
    process.ecalPreshowerDigis = cms.EDProducer("ESRawToDigi",
        ESdigiCollection = cms.string(''),
        InstanceES = cms.string(''),
        LookupTable = cms.FileInPath('EventFilter/ESDigiToRaw/data/ES_lookup_table.dat'),
        debugMode = cms.untracked.bool(False),
        sourceTag = cms.InputTag("rawDataCollector")
    )


    process.ecalPreshowerRecHit = cms.EDProducer("ESRecHitProducer",
        ESRecoAlgo = cms.int32(0),
        ESdigiCollection = cms.InputTag("ecalPreshowerDigis"),
        ESrechitCollection = cms.string('EcalRecHitsES'),
        algo = cms.string('ESRecHitWorker')
    )


    #Ecal naming taken from offline 
    process.HLTDoFullUnpackingEgammaEcalMFSequence = cms.Sequence( process.ecalDigis + 
                                                                   process.ecalPreshowerDigis + 
                                                                   process.ecalMultiFitUncalibRecHit+
                                                                   process.ecalDetIdToBeRecovered + 
                                                                   process.ecalRecHit + 
                                                                   process.ecalPreshowerRecHit )

    process.HLTDoLocalHcalSequence = cms.Sequence( process.hcalDigis + 
                                                   process.hbhereco + 
                                                   process.hfprereco + 
                                                   process.hfreco + 
                                                   process.horeco )

    process.hltTowerMakerForECALMF = cms.EDProducer( "CaloTowersCreator",
        EBSumThreshold = cms.double( 0.2 ),
        MomHBDepth = cms.double( 0.2 ),
        UseEtEBTreshold = cms.bool( False ),
        hfInput = cms.InputTag( "hfreco" ),
        AllowMissingInputs = cms.bool( False ),
        HEDThreshold1 = cms.double( 0.8 ),
        MomEEDepth = cms.double( 0.0 ),
        EESumThreshold = cms.double( 0.45 ),
        HBGrid = cms.vdouble(  ),
        HcalAcceptSeverityLevelForRejectedHit = cms.uint32( 9999 ),
        HBThreshold = cms.double( 0.7 ),
        EcalSeveritiesToBeUsedInBadTowers = cms.vstring(  ),
        UseEcalRecoveredHits = cms.bool( False ),
        MomConstrMethod = cms.int32( 1 ),
        MomHEDepth = cms.double( 0.4 ),
        HcalThreshold = cms.double( -1000.0 ),
        HF2Weights = cms.vdouble( 1.0E-99 ),
        HOWeights = cms.vdouble( 1.0E-99 ),
        EEGrid = cms.vdouble(  ),
        UseSymEBTreshold = cms.bool( False ),
        EEWeights = cms.vdouble(  ),
        EEWeight = cms.double( 1.0 ),
        UseHO = cms.bool( False ),
        HBWeights = cms.vdouble( 1.0E-99 ),
        HF1Weight = cms.double( 1.0E-99 ),
        HF2Grid = cms.vdouble(  ),
        HESThreshold1 = cms.double( 0.8 ),
        HEDWeights = cms.vdouble( 1.0E-99 ),
        EBWeight = cms.double( 1.0 ),
        HF1Grid = cms.vdouble(  ),
        EBWeights = cms.vdouble(  ),
        HOWeight = cms.double( 1.0E-99 ),
        HESWeight = cms.double( 1.0E-99 ),
        HESThreshold = cms.double( 0.8 ),
        hbheInput = cms.InputTag( "hbhereco" ),
        HF2Weight = cms.double( 1.0E-99 ),
        HF2Threshold = cms.double( 0.85 ),
        HcalAcceptSeverityLevel = cms.uint32( 9 ),
        EEThreshold = cms.double( 0.3 ),
        HOThresholdPlus1 = cms.double( 3.5 ),
        HOThresholdPlus2 = cms.double( 3.5 ),
        HF1Weights = cms.vdouble( 1.0E-99 ),
        hoInput = cms.InputTag( "horeco" ),
        HF1Threshold = cms.double( 0.5 ),
        HcalPhase = cms.int32( 0 ),
        HESGrid = cms.vdouble(  ),
        EcutTower = cms.double( -1000.0 ),
        UseRejectedRecoveredEcalHits = cms.bool( False ),
        UseEtEETreshold = cms.bool( False ),
        HESWeights = cms.vdouble( 1.0E-99 ),
        HOThresholdMinus1 = cms.double( 3.5 ),
        EcalRecHitSeveritiesToBeExcluded = cms.vstring( 'kTime',
          'kWeird',
          'kBad' ),
        HEDWeight = cms.double( 1.0E-99 ),
        UseSymEETreshold = cms.bool( False ),
        HEDThreshold = cms.double( 0.8 ),
        UseRejectedHitsOnly = cms.bool( False ),
        EBThreshold = cms.double( 0.07 ),
        HEDGrid = cms.vdouble(  ),
        UseHcalRecoveredHits = cms.bool( False ),
        HOThresholdMinus2 = cms.double( 3.5 ),
        HOThreshold0 = cms.double( 3.5 ),
        ecalInputs = cms.VInputTag( 'ecalRecHit:EcalRecHitsEB','ecalRecHit:EcalRecHitsEE' ),
        UseRejectedRecoveredHcalHits = cms.bool( False ),
        MomEBDepth = cms.double( 0.3 ),
        HBWeight = cms.double( 1.0E-99 ),
        HOGrid = cms.vdouble(  ),
        EBGrid = cms.vdouble(  )
    )
    process.hltTowerMakerForHCAL = cms.EDProducer( "CaloTowersCreator",
        EBSumThreshold = cms.double( 0.2 ),
        MomHBDepth = cms.double( 0.2 ),
        UseEtEBTreshold = cms.bool( False ),
        hfInput = cms.InputTag( "hfreco" ),
        AllowMissingInputs = cms.bool( False ),
        HEDThreshold1 = cms.double( 0.8 ),
        MomEEDepth = cms.double( 0.0 ),
        EESumThreshold = cms.double( 0.45 ),
        HBGrid = cms.vdouble(  ),
        HcalAcceptSeverityLevelForRejectedHit = cms.uint32( 9999 ),
        HBThreshold = cms.double( 0.7 ),
        EcalSeveritiesToBeUsedInBadTowers = cms.vstring(  ),
        UseEcalRecoveredHits = cms.bool( False ),
        MomConstrMethod = cms.int32( 1 ),
        MomHEDepth = cms.double( 0.4 ),
        HcalThreshold = cms.double( -1000.0 ),
        HF2Weights = cms.vdouble(  ),
        HOWeights = cms.vdouble(  ),
        EEGrid = cms.vdouble(  ),
        UseSymEBTreshold = cms.bool( False ),
        EEWeights = cms.vdouble( 1.0E-99 ),
        EEWeight = cms.double( 1.0E-99 ),
        UseHO = cms.bool( False ),
        HBWeights = cms.vdouble(  ),
        HF1Weight = cms.double( 1.0 ),
        HF2Grid = cms.vdouble(  ),
        HESThreshold1 = cms.double( 0.8 ),
        HEDWeights = cms.vdouble(  ),
        EBWeight = cms.double( 1.0E-99 ),
        HF1Grid = cms.vdouble(  ),
        EBWeights = cms.vdouble( 1.0E-99 ),
        HOWeight = cms.double( 1.0E-99 ),
        HESWeight = cms.double( 1.0 ),
        HESThreshold = cms.double( 0.8 ),
        hbheInput = cms.InputTag( "hbhereco" ),
        HF2Weight = cms.double( 1.0 ),
        HF2Threshold = cms.double( 0.85 ),
        HcalAcceptSeverityLevel = cms.uint32( 9 ),
        EEThreshold = cms.double( 0.3 ),
        HOThresholdPlus1 = cms.double( 3.5 ),
        HOThresholdPlus2 = cms.double( 3.5 ),
        HF1Weights = cms.vdouble(  ),
        hoInput = cms.InputTag( "horeco" ),
        HF1Threshold = cms.double( 0.5 ),
        HcalPhase = cms.int32( 0 ),
        HESGrid = cms.vdouble(  ),
        EcutTower = cms.double( -1000.0 ),
        UseRejectedRecoveredEcalHits = cms.bool( False ),
        UseEtEETreshold = cms.bool( False ),
        HESWeights = cms.vdouble(  ),
        HOThresholdMinus1 = cms.double( 3.5 ),
        EcalRecHitSeveritiesToBeExcluded = cms.vstring( 'kTime',
          'kWeird',
          'kBad' ),
        HEDWeight = cms.double( 1.0 ),
        UseSymEETreshold = cms.bool( False ),
        HEDThreshold = cms.double( 0.8 ),
        UseRejectedHitsOnly = cms.bool( False ),
        EBThreshold = cms.double( 0.07 ),
        HEDGrid = cms.vdouble(  ),
        UseHcalRecoveredHits = cms.bool( False ),
        HOThresholdMinus2 = cms.double( 3.5 ),
        HOThreshold0 = cms.double( 3.5 ),
        ecalInputs = cms.VInputTag( 'ecalRecHit:EcalRecHitsEB','ecalRecHit:EcalRecHitsEE' ),
        UseRejectedRecoveredHcalHits = cms.bool( False ),
        MomEBDepth = cms.double( 0.3 ),
        HBWeight = cms.double( 1.0 ),
        HOGrid = cms.vdouble(  ),
        EBGrid = cms.vdouble(  )
    )
    process.hltFixedGridRhoFastjetECALMFForMuons = cms.EDProducer( "FixedGridRhoProducerFastjet",
        gridSpacing = cms.double( 0.55 ),
        maxRapidity = cms.double( 2.5 ),
        pfCandidatesTag = cms.InputTag( "hltTowerMakerForECALMF" )
    )
    process.hltFixedGridRhoFastjetHCAL = cms.EDProducer( "FixedGridRhoProducerFastjet",
        gridSpacing = cms.double( 0.55 ),
        maxRapidity = cms.double( 2.5 ),
        pfCandidatesTag = cms.InputTag( "hltTowerMakerForHCAL" )
    )
    process.hltRecHitInRegionForMuonsMF = cms.EDProducer( "MuonHLTRechitInRegionsProducer",
        l1LowerThr = cms.double( 0.0 ),
        doIsolated = cms.bool( True ),
        useUncalib = cms.bool( False ),
        regionEtaMargin = cms.double( 0.4 ),
        ecalhitLabels = cms.VInputTag( 'ecalRecHit:EcalRecHitsEB','ecalRecHit:EcalRecHitsEE' ),
        regionPhiMargin = cms.double( 0.4 ),
        l1TagNonIsolated = cms.InputTag( "NotUsed" ),
        l1UpperThr = cms.double( 999.0 ),
        l1LowerThrIgnoreIsolation = cms.double( 100.0 ),
        productLabels = cms.vstring( 'EcalRegionalRecHitsEB','EcalRegionalRecHitsEE' ),
        l1TagIsolated = cms.InputTag( "hltIterL3MuonCandidates" )
    )
    process.hltRecHitInRegionForMuonsES = cms.EDProducer( "MuonHLTRechitInRegionsProducer",
        l1LowerThr = cms.double( 0.0 ),
        doIsolated = cms.bool( True ),
        useUncalib = cms.bool( False ),
        regionEtaMargin = cms.double( 0.4 ),
        ecalhitLabels = cms.VInputTag( 'ecalPreshowerRecHit:EcalRecHitsES' ),
        regionPhiMargin = cms.double( 0.4 ),
        l1TagNonIsolated = cms.InputTag( "NotUsed" ),
        l1UpperThr = cms.double( 999.0 ),
        l1LowerThrIgnoreIsolation = cms.double( 100.0 ),
        productLabels = cms.vstring( 'EcalRegionalRecHitsES' ),
        l1TagIsolated = cms.InputTag( "hltIterL3MuonCandidates" )
    )
    process.hltParticleFlowRecHitECALForMuonsMF = cms.EDProducer( "PFRecHitProducer",
        producers = cms.VPSet( 
          cms.PSet(  src = cms.InputTag( 'hltRecHitInRegionForMuonsMF','EcalRegionalRecHitsEB' ),
            srFlags = cms.InputTag( "" ),
            name = cms.string( "PFEBRecHitCreator" ),
            qualityTests = cms.VPSet( 
              cms.PSet(  thresholds = cms.vdouble( 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.11, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.17, 0.18, 0.18, 0.19, 0.19, 0.2, 0.22, 0.23, 0.25, 0.27, 0.29, 0.31, 0.34, 0.36, 0.39, 0.42, 0.45, 0.5, 0.57, 0.68, 0.84, 1.07, 1.4, 1.88, 2.55, 3.47, 4.73, 6.42, 8.65, 11.6, 15.4, 0.11, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.17, 0.18, 0.18, 0.19, 0.19, 0.2, 0.22, 0.23, 0.25, 0.27, 0.29, 0.31, 0.34, 0.36, 0.39, 0.42, 0.45, 0.5, 0.57, 0.68, 0.84, 1.07, 1.4, 1.88, 2.55, 3.47, 4.73, 6.42, 8.65, 11.6, 15.4 ),
                name = cms.string( "PFRecHitQTestECALMultiThreshold" ),
                applySelectionsToAllCrystals = cms.bool( True )
              ),
              cms.PSet(  topologicalCleaning = cms.bool( True ),
                skipTTRecoveredHits = cms.bool( True ),
                cleaningThreshold = cms.double( 2.0 ),
                name = cms.string( "PFRecHitQTestECAL" ),
                timingCleaning = cms.bool( True )
              )
            )
          ),
          cms.PSet(  src = cms.InputTag( 'hltRecHitInRegionForMuonsMF','EcalRegionalRecHitsEE' ),
            srFlags = cms.InputTag( "" ),
            name = cms.string( "PFEERecHitCreator" ),
            qualityTests = cms.VPSet( 
              cms.PSet(  thresholds = cms.vdouble( 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.14, 0.11, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.17, 0.18, 0.18, 0.19, 0.19, 0.2, 0.22, 0.23, 0.25, 0.27, 0.29, 0.31, 0.34, 0.36, 0.39, 0.42, 0.45, 0.5, 0.57, 0.68, 0.84, 1.07, 1.4, 1.88, 2.55, 3.47, 4.73, 6.42, 8.65, 11.6, 15.4, 0.11, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.17, 0.17, 0.18, 0.18, 0.19, 0.19, 0.2, 0.22, 0.23, 0.25, 0.27, 0.29, 0.31, 0.34, 0.36, 0.39, 0.42, 0.45, 0.5, 0.57, 0.68, 0.84, 1.07, 1.4, 1.88, 2.55, 3.47, 4.73, 6.42, 8.65, 11.6, 15.4 ),
                name = cms.string( "PFRecHitQTestECALMultiThreshold" ),
                applySelectionsToAllCrystals = cms.bool( True )
              ),
              cms.PSet(  topologicalCleaning = cms.bool( True ),
                skipTTRecoveredHits = cms.bool( True ),
                cleaningThreshold = cms.double( 2.0 ),
                name = cms.string( "PFRecHitQTestECAL" ),
                timingCleaning = cms.bool( True )
              )
            )
          )
        ),
        navigator = cms.PSet( 
          barrel = cms.PSet(  ),
          endcap = cms.PSet(  ),
          name = cms.string( "PFRecHitECALNavigator" )
        )
    )
    process.hltParticleFlowRecHitPSForMuons = cms.EDProducer( "PFRecHitProducer",
        producers = cms.VPSet( 
          cms.PSet(  src = cms.InputTag( 'hltRecHitInRegionForMuonsES','EcalRegionalRecHitsES' ),
            name = cms.string( "PFPSRecHitCreator" ),
            qualityTests = cms.VPSet( 
              cms.PSet(  threshold = cms.double( 7.0E-6 ),
                name = cms.string( "PFRecHitQTestThreshold" )
              )
            )
          )
        ),
        navigator = cms.PSet(  name = cms.string( "PFRecHitPreshowerNavigator" ) )
    )
    process.hltParticleFlowClusterECALUncorrectedForMuonsMF = cms.EDProducer( "PFClusterProducer",
        pfClusterBuilder = cms.PSet( 
          minFracTot = cms.double( 1.0E-20 ),
          stoppingTolerance = cms.double( 1.0E-8 ),
          positionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( 9 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 0.08 ),
            minFractionInCalc = cms.double( 1.0E-9 ),
            timeResolutionCalcBarrel = cms.PSet( 
              corrTermLowE = cms.double( 0.0510871 ),
              threshLowE = cms.double( 0.5 ),
              noiseTerm = cms.double( 1.10889 ),
              constantTermLowE = cms.double( 0.0 ),
              noiseTermLowE = cms.double( 1.31883 ),
              threshHighE = cms.double( 5.0 ),
              constantTerm = cms.double( 0.428192 )
            ),
            timeResolutionCalcEndcap = cms.PSet( 
              corrTermLowE = cms.double( 0.0 ),
              threshLowE = cms.double( 1.0 ),
              noiseTerm = cms.double( 5.72489999999 ),
              constantTermLowE = cms.double( 0.0 ),
              noiseTermLowE = cms.double( 6.92683000001 ),
              threshHighE = cms.double( 10.0 ),
              constantTerm = cms.double( 0.0 )
            )
          ),
          maxIterations = cms.uint32( 50 ),
          positionCalcForConvergence = cms.PSet( 
            minAllowedNormalization = cms.double( 0.0 ),
            T0_ES = cms.double( 1.2 ),
            algoName = cms.string( "ECAL2DPositionCalcWithDepthCorr" ),
            T0_EE = cms.double( 3.1 ),
            T0_EB = cms.double( 7.4 ),
            X0 = cms.double( 0.89 ),
            minFractionInCalc = cms.double( 0.0 ),
            W0 = cms.double( 4.2 )
          ),
          allCellsPositionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( -1 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 0.08 ),
            minFractionInCalc = cms.double( 1.0E-9 ),
            timeResolutionCalcBarrel = cms.PSet( 
              corrTermLowE = cms.double( 0.0510871 ),
              threshLowE = cms.double( 0.5 ),
              noiseTerm = cms.double( 1.10889 ),
              constantTermLowE = cms.double( 0.0 ),
              noiseTermLowE = cms.double( 1.31883 ),
              threshHighE = cms.double( 5.0 ),
              constantTerm = cms.double( 0.428192 )
            ),
            timeResolutionCalcEndcap = cms.PSet( 
              corrTermLowE = cms.double( 0.0 ),
              threshLowE = cms.double( 1.0 ),
              noiseTerm = cms.double( 5.72489999999 ),
              constantTermLowE = cms.double( 0.0 ),
              noiseTermLowE = cms.double( 6.92683000001 ),
              threshHighE = cms.double( 10.0 ),
              constantTerm = cms.double( 0.0 )
            )
          ),
          algoName = cms.string( "Basic2DGenericPFlowClusterizer" ),
          recHitEnergyNorms = cms.VPSet( 
            cms.PSet(  recHitEnergyNorm = cms.double( 0.08 ),
              detector = cms.string( "ECAL_BARREL" )
            ),
            cms.PSet(  recHitEnergyNorm = cms.double( 0.3 ),
              detector = cms.string( "ECAL_ENDCAP" )
            )
          ),
          showerSigma = cms.double( 1.5 ),
          minFractionToKeep = cms.double( 1.0E-7 ),
          excludeOtherSeeds = cms.bool( True )
        ),
        positionReCalc = cms.PSet( 
          minAllowedNormalization = cms.double( 0.0 ),
          T0_ES = cms.double( 1.2 ),
          algoName = cms.string( "ECAL2DPositionCalcWithDepthCorr" ),
          T0_EE = cms.double( 3.1 ),
          T0_EB = cms.double( 7.4 ),
          X0 = cms.double( 0.89 ),
          minFractionInCalc = cms.double( 0.0 ),
          W0 = cms.double( 4.2 )
        ),
        initialClusteringStep = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  gatheringThreshold = cms.double( 0.08 ),
              gatheringThresholdPt = cms.double( 0.0 ),
              detector = cms.string( "ECAL_BARREL" )
            ),
            cms.PSet(  gatheringThreshold = cms.double( 0.3 ),
              gatheringThresholdPt = cms.double( 0.0 ),
              detector = cms.string( "ECAL_ENDCAP" )
            )
          ),
          algoName = cms.string( "Basic2DGenericTopoClusterizer" ),
          useCornerCells = cms.bool( True )
        ),
        energyCorrector = cms.PSet(  ),
        recHitCleaners = cms.VPSet( 
        ),
        seedFinder = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  seedingThresholdPt = cms.double( 0.15 ),
              seedingThreshold = cms.double( 0.6 ),
              detector = cms.string( "ECAL_ENDCAP" )
            ),
            cms.PSet(  seedingThresholdPt = cms.double( 0.0 ),
              seedingThreshold = cms.double( 0.23 ),
              detector = cms.string( "ECAL_BARREL" )
            )
          ),
          algoName = cms.string( "LocalMaximumSeedFinder" ),
          nNeighbours = cms.int32( 8 )
        ),
        recHitsSource = cms.InputTag( "hltParticleFlowRecHitECALForMuonsMF" )
    )
    process.hltParticleFlowClusterPSForMuons = cms.EDProducer( "PFClusterProducer",
        pfClusterBuilder = cms.PSet( 
          minFracTot = cms.double( 1.0E-20 ),
          stoppingTolerance = cms.double( 1.0E-8 ),
          positionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( -1 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 6.0E-5 ),
            minFractionInCalc = cms.double( 1.0E-9 )
          ),
          maxIterations = cms.uint32( 50 ),
          algoName = cms.string( "Basic2DGenericPFlowClusterizer" ),
          recHitEnergyNorms = cms.VPSet( 
            cms.PSet(  recHitEnergyNorm = cms.double( 6.0E-5 ),
              detector = cms.string( "PS1" )
            ),
            cms.PSet(  recHitEnergyNorm = cms.double( 6.0E-5 ),
              detector = cms.string( "PS2" )
            )
          ),
          showerSigma = cms.double( 0.3 ),
          minFractionToKeep = cms.double( 1.0E-7 ),
          excludeOtherSeeds = cms.bool( True )
        ),
        positionReCalc = cms.PSet(  ),
        initialClusteringStep = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  gatheringThreshold = cms.double( 6.0E-5 ),
              gatheringThresholdPt = cms.double( 0.0 ),
              detector = cms.string( "PS1" )
            ),
            cms.PSet(  gatheringThreshold = cms.double( 6.0E-5 ),
              gatheringThresholdPt = cms.double( 0.0 ),
              detector = cms.string( "PS2" )
            )
          ),
          algoName = cms.string( "Basic2DGenericTopoClusterizer" ),
          useCornerCells = cms.bool( False )
        ),
        energyCorrector = cms.PSet(  ),
        recHitCleaners = cms.VPSet( 
        ),
        seedFinder = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  seedingThresholdPt = cms.double( 0.0 ),
              seedingThreshold = cms.double( 1.2E-4 ),
              detector = cms.string( "PS1" )
            ),
            cms.PSet(  seedingThresholdPt = cms.double( 0.0 ),
              seedingThreshold = cms.double( 1.2E-4 ),
              detector = cms.string( "PS2" )
            )
          ),
          algoName = cms.string( "LocalMaximumSeedFinder" ),
          nNeighbours = cms.int32( 4 )
        ),
        recHitsSource = cms.InputTag( "hltParticleFlowRecHitPSForMuons" )
    )
    process.hltParticleFlowClusterECALForMuonsMF = cms.EDProducer( "CorrectedECALPFClusterProducer",
        inputPS = cms.InputTag( "hltParticleFlowClusterPSForMuons" ),
        minimumPSEnergy = cms.double( 0.0 ),
        energyCorrector = cms.PSet( 
          applyCrackCorrections = cms.bool( False )
        ),
        inputECAL = cms.InputTag( "hltParticleFlowClusterECALUncorrectedForMuonsMF" )
    )
    process.hltMuonEcalMFPFClusterIsoForMuons = cms.EDProducer( "MuonHLTEcalPFClusterIsolationProducer",
        effectiveAreas = cms.vdouble( 0.35, 0.193 ),
        doRhoCorrection = cms.bool( True ),
        etaStripBarrel = cms.double( 0.0 ),
        energyEndcap = cms.double( 0.0 ),
        rhoProducer = cms.InputTag( "hltFixedGridRhoFastjetECALMFForMuons" ),
        pfClusterProducer = cms.InputTag( "hltParticleFlowClusterECALForMuonsMF" ),
        etaStripEndcap = cms.double( 0.0 ),
        drVetoBarrel = cms.double( 0.05 ),
        drMax = cms.double( 0.3 ),
        energyBarrel = cms.double( 0.0 ),
        absEtaLowEdges = cms.vdouble( 0.0, 1.479 ),
        drVetoEndcap = cms.double( 0.05 ),
        rhoMax = cms.double( 9.9999999E7 ),
        rhoScale = cms.double( 1.0 ),
        recoCandidateProducer = cms.InputTag( "hltIterL3MuonCandidates" )
    )
    process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFilteredEB0p14EE0p10 = cms.EDFilter( "HLTMuonGenericFilter",
        thrOverE2EE = cms.vdouble( -1.0 ),
        effectiveAreas = cms.vdouble( 0.0, 0.0 ),
        energyLowEdges = cms.vdouble( 0.0 ),
        doRhoCorrection = cms.bool( False ),
        saveTags = cms.bool( True ),
        thrOverE2EB = cms.vdouble( -1.0 ),
        thrRegularEE = cms.vdouble( -1.0 ),
        thrOverEEE = cms.vdouble( 0.1 ),
        varTag = cms.InputTag( "hltMuonEcalMFPFClusterIsoForMuons" ),
        thrOverEEB = cms.vdouble( 0.14 ),
        thrRegularEB = cms.vdouble( -1.0 ),
        lessThan = cms.bool( True ),
        l1EGCand = cms.InputTag( "hltIterL3MuonCandidates" ),
        ncandcut = cms.int32( 1 ),
        absEtaLowEdges = cms.vdouble( 0.0, 1.479 ),
        candTag = cms.InputTag( "hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q" ),
        rhoTag = cms.InputTag( "" ),
        rhoMax = cms.double( 9.9999999E7 ),
        useEt = cms.bool( True ),
        rhoScale = cms.double( 1.0 )
    )



    process.HLTPFClusteringEcalMFForMuons = cms.Sequence( process.hltRecHitInRegionForMuonsMF + process.hltRecHitInRegionForMuonsES + process.hltParticleFlowRecHitECALForMuonsMF + process.hltParticleFlowRecHitPSForMuons + process.hltParticleFlowClusterECALUncorrectedForMuonsMF + process.hltParticleFlowClusterPSForMuons + process.hltParticleFlowClusterECALForMuonsMF )

    process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence( process.HLTDoFullUnpackingEgammaEcalMFSequence + process.HLTDoLocalHcalSequence + 
                                                                          process.hltTowerMakerForECALMF + process.hltTowerMakerForHCAL + 
                                                                          process.hltFixedGridRhoFastjetECALMFForMuons + process.hltFixedGridRhoFastjetHCAL + 
                                                                          process.HLTPFClusteringEcalMFForMuons + process.hltMuonEcalMFPFClusterIsoForMuons )




    process.hltRegionalTowerForMuonsReg = cms.EDProducer( "EgammaHLTCaloTowerProducer",
        L1NonIsoCand = cms.InputTag( "hltIterL3MuonCandidates" ),
        EMin = cms.double( 0.0 ),
        EtMin = cms.double( 0.0 ),
        L1IsoCand = cms.InputTag( "hltIterL3MuonCandidates" ),
        useTowersInCone = cms.double( 0.8 ),
        towerCollection = cms.InputTag( "hltTowerMakerForHCAL" )
    )
    process.hltParticleFlowRecHitHBHERegForMuons = cms.EDProducer( "PFRecHitProducer",
        producers = cms.VPSet( 
          cms.PSet(  src = cms.InputTag( "hbhereco" ),
            name = cms.string( "PFHBHERecHitCreator" ),
            qualityTests = cms.VPSet( 
              cms.PSet(  threshold = cms.double( 0.8 ),
                name = cms.string( "PFRecHitQTestThreshold" ),
                cuts = cms.VPSet( 
                  cms.PSet(  depth = cms.vint32( 1, 2, 3, 4 ),
                    threshold = cms.vdouble( 0.8, 0.8, 0.8, 0.8 ),
                    detectorEnum = cms.int32( 1 )
                  ),
                  cms.PSet(  depth = cms.vint32( 1, 2, 3, 4, 5, 6, 7 ),
                    threshold = cms.vdouble( 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8 ),
                    detectorEnum = cms.int32( 2 )
                  )
                )
              ),
              cms.PSet(  flags = cms.vstring( 'Standard' ),
                cleaningThresholds = cms.vdouble( 0.0 ),
                name = cms.string( "PFRecHitQTestHCALChannel" ),
                maxSeverities = cms.vint32( 11 )
              )
            )
          )
        ),
        navigator = cms.PSet( 
          name = cms.string( "PFRecHitHCALNavigator" ),
          sigmaCut = cms.double( 4.0 ),
          timeResolutionCalc = cms.PSet( 
            corrTermLowE = cms.double( 0.0 ),
            threshLowE = cms.double( 2.0 ),
            noiseTerm = cms.double( 8.64 ),
            constantTermLowE = cms.double( 6.0 ),
            noiseTermLowE = cms.double( 0.0 ),
            threshHighE = cms.double( 8.0 ),
            constantTerm = cms.double( 1.92 )
          )
        )
    )
    process.hltParticleFlowClusterHBHERegForMuons = cms.EDProducer( "PFClusterProducer",
        pfClusterBuilder = cms.PSet( 
          minFracTot = cms.double( 1.0E-20 ),
          stoppingTolerance = cms.double( 1.0E-8 ),
          positionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( 5 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 0.8 ),
            minFractionInCalc = cms.double( 1.0E-9 )
          ),
          maxIterations = cms.uint32( 50 ),
          minChi2Prob = cms.double( 0.0 ),
          allCellsPositionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( -1 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 0.8 ),
            minFractionInCalc = cms.double( 1.0E-9 )
          ),
          algoName = cms.string( "Basic2DGenericPFlowClusterizer" ),
          recHitEnergyNorms = cms.VPSet( 
            cms.PSet(  detector = cms.string( "HCAL_BARREL1" ),
              depths = cms.vint32( 1, 2, 3, 4 ),
              recHitEnergyNorm = cms.vdouble( 0.8, 0.8, 0.8, 0.8 )
            ),
            cms.PSet(  detector = cms.string( "HCAL_ENDCAP" ),
              depths = cms.vint32( 1, 2, 3, 4, 5, 6, 7 ),
              recHitEnergyNorm = cms.vdouble( 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8 )
            )
          ),
          maxNSigmaTime = cms.double( 10.0 ),
          showerSigma = cms.double( 10.0 ),
          timeSigmaEE = cms.double( 10.0 ),
          clusterTimeResFromSeed = cms.bool( False ),
          minFractionToKeep = cms.double( 1.0E-7 ),
          excludeOtherSeeds = cms.bool( True ),
          timeResolutionCalcBarrel = cms.PSet( 
            corrTermLowE = cms.double( 0.0 ),
            threshLowE = cms.double( 6.0 ),
            noiseTerm = cms.double( 21.86 ),
            constantTermLowE = cms.double( 4.24 ),
            noiseTermLowE = cms.double( 8.0 ),
            threshHighE = cms.double( 15.0 ),
            constantTerm = cms.double( 2.82 )
          ),
          timeResolutionCalcEndcap = cms.PSet( 
            corrTermLowE = cms.double( 0.0 ),
            threshLowE = cms.double( 6.0 ),
            noiseTerm = cms.double( 21.86 ),
            constantTermLowE = cms.double( 4.24 ),
            noiseTermLowE = cms.double( 8.0 ),
            threshHighE = cms.double( 15.0 ),
            constantTerm = cms.double( 2.82 )
          ),
          timeSigmaEB = cms.double( 10.0 )
        ),
        positionReCalc = cms.PSet(  ),
        initialClusteringStep = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  detector = cms.string( "HCAL_BARREL1" ),
              depths = cms.vint32( 1, 2, 3, 4 ),
              gatheringThreshold = cms.vdouble( 0.8, 0.8, 0.8, 0.8 ),
              gatheringThresholdPt = cms.vdouble( 0.0, 0.0, 0.0, 0.0 )
            ),
            cms.PSet(  detector = cms.string( "HCAL_ENDCAP" ),
              depths = cms.vint32( 1, 2, 3, 4, 5, 6, 7 ),
              gatheringThreshold = cms.vdouble( 0.8, 0.8, 0.8, 0.8, 0.8, 0.8, 0.8 ),
              gatheringThresholdPt = cms.vdouble( 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 )
            )
          ),
          algoName = cms.string( "Basic2DGenericTopoClusterizer" ),
          useCornerCells = cms.bool( True )
        ),
        energyCorrector = cms.PSet(  ),
        recHitCleaners = cms.VPSet( 
        ),
        seedFinder = cms.PSet( 
          thresholdsByDetector = cms.VPSet( 
            cms.PSet(  detector = cms.string( "HCAL_BARREL1" ),
              depths = cms.vint32( 1, 2, 3, 4 ),
              seedingThreshold = cms.vdouble( 1.0, 1.0, 1.0, 1.0 ),
              seedingThresholdPt = cms.vdouble( 0.0, 0.0, 0.0, 0.0 )
            ),
            cms.PSet(  detector = cms.string( "HCAL_ENDCAP" ),
              depths = cms.vint32( 1, 2, 3, 4, 5, 6, 7 ),
              seedingThreshold = cms.vdouble( 1.1, 1.1, 1.1, 1.1, 1.1, 1.1, 1.1 ),
              seedingThresholdPt = cms.vdouble( 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0 )
            )
          ),
          algoName = cms.string( "LocalMaximumSeedFinder" ),
          nNeighbours = cms.int32( 4 )
        ),
        recHitsSource = cms.InputTag( "hltParticleFlowRecHitHBHERegForMuons" )
    )
    process.hltParticleFlowClusterHCALRegForMuons = cms.EDProducer( "PFMultiDepthClusterProducer",
        pfClusterBuilder = cms.PSet( 
          allCellsPositionCalc = cms.PSet( 
            minAllowedNormalization = cms.double( 1.0E-9 ),
            posCalcNCrystals = cms.int32( -1 ),
            algoName = cms.string( "Basic2DGenericPFlowPositionCalc" ),
            logWeightDenominator = cms.double( 0.8 ),
            minFractionInCalc = cms.double( 1.0E-9 )
          ),
          algoName = cms.string( "PFMultiDepthClusterizer" ),
          nSigmaPhi = cms.double( 2.0 ),
          minFractionToKeep = cms.double( 1.0E-7 ),
          nSigmaEta = cms.double( 2.0 )
        ),
        energyCorrector = cms.PSet(  ),
        positionReCalc = cms.PSet(  ),
        clustersSource = cms.InputTag( "hltParticleFlowClusterHBHERegForMuons" )
    )
    process.hltMuonHcalRegPFClusterIsoForMuons = cms.EDProducer( "MuonHLTHcalPFClusterIsolationProducer",
        effectiveAreas = cms.vdouble( 0.227, 0.372 ),
        useHF = cms.bool( False ),
        useEt = cms.bool( True ),
        etaStripBarrel = cms.double( 0.0 ),
        pfClusterProducerHFHAD = cms.InputTag( "" ),
        energyEndcap = cms.double( 0.0 ),
        rhoProducer = cms.InputTag( "hltFixedGridRhoFastjetHCAL" ),
        etaStripEndcap = cms.double( 0.0 ),
        drVetoBarrel = cms.double( 0.1 ),
        pfClusterProducerHCAL = cms.InputTag( "hltParticleFlowClusterHCALRegForMuons" ),
        drMax = cms.double( 0.3 ),
        doRhoCorrection = cms.bool( True ),
        energyBarrel = cms.double( 0.0 ),
        absEtaLowEdges = cms.vdouble( 0.0, 1.479 ),
        drVetoEndcap = cms.double( 0.1 ),
        rhoMax = cms.double( 9.9999999E7 ),
        pfClusterProducerHFEM = cms.InputTag( "" ),
        rhoScale = cms.double( 1.0 ),
        recoCandidateProducer = cms.InputTag( "hltIterL3MuonCandidates" )
    )
    process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFilteredHB0p16HE0p20 = cms.EDFilter( "HLTMuonGenericFilter",
        thrOverE2EE = cms.vdouble( -1.0 ),
        effectiveAreas = cms.vdouble( 0.0, 0.0 ),
        energyLowEdges = cms.vdouble( 0.0 ),
        doRhoCorrection = cms.bool( False ),
        saveTags = cms.bool( True ),
        thrOverE2EB = cms.vdouble( -1.0 ),
        thrRegularEE = cms.vdouble( -1.0 ),
        thrOverEEE = cms.vdouble( 0.2 ),
        varTag = cms.InputTag( "hltMuonHcalRegPFClusterIsoForMuons" ),
        thrOverEEB = cms.vdouble( 0.16 ),
        thrRegularEB = cms.vdouble( -1.0 ),
        lessThan = cms.bool( True ),
        l1EGCand = cms.InputTag( "hltIterL3MuonCandidates" ),
        ncandcut = cms.int32( 1 ),
        absEtaLowEdges = cms.vdouble( 0.0, 1.479 ),
        candTag = cms.InputTag( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFilteredEB0p14EE0p10" ),
        rhoTag = cms.InputTag( "" ),
        rhoMax = cms.double( 9.9999999E7 ),
        useEt = cms.bool( True ),
        rhoScale = cms.double( 1.0 )
    )

    process.HLTPFHcalRegClusteringForMuons = cms.Sequence( process.hltRegionalTowerForMuonsReg + process.hltParticleFlowRecHitHBHERegForMuons + process.hltParticleFlowClusterHBHERegForMuons + process.hltParticleFlowClusterHCALRegForMuons )

    process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence( process.HLTPFHcalRegClusteringForMuons + 
                                                                          process.hltMuonHcalRegPFClusterIsoForMuons )



    #################################
    ### processes for HGCal Isolation
    #################################

    process.hgcalDigis = cms.EDProducer("HGCalRawToDigiFake",
        bhDigis = cms.InputTag("simHGCalUnsuppressedDigis","HEback"),
        eeDigis = cms.InputTag("simHGCalUnsuppressedDigis","EE"),
        fhDigis = cms.InputTag("simHGCalUnsuppressedDigis","HEfront"),
        mightGet = cms.optional.untracked.vstring
    )

    process.HGCalUncalibRecHit = cms.EDProducer("HGCalUncalibRecHitProducer",
        HGCEEConfig = cms.PSet(
            adcNbits = cms.uint32(10),
            adcSaturation = cms.double(100),
            fCPerMIP = cms.vdouble(2.06, 3.43, 5.15),
            isSiFE = cms.bool(True),
            tdcNbits = cms.uint32(12),
            tdcOnset = cms.double(60),
            tdcSaturation = cms.double(10000),
            toaLSB_ns = cms.double(0.0244)
        ),
        HGCEEdigiCollection = cms.InputTag("hgcalDigis","EE"),
        HGCEEhitCollection = cms.string('HGCEEUncalibRecHits'),
        HGCHEBConfig = cms.PSet(
            adcNbits = cms.uint32(10),
            adcSaturation = cms.double(68.75),
            fCPerMIP = cms.vdouble(1.0, 1.0, 1.0),
            isSiFE = cms.bool(True),
            tdcNbits = cms.uint32(12),
            tdcOnset = cms.double(55),
            tdcSaturation = cms.double(1000),
            toaLSB_ns = cms.double(0.0244)
        ),
        HGCHEBdigiCollection = cms.InputTag("hgcalDigis","HEback"),
        HGCHEBhitCollection = cms.string('HGCHEBUncalibRecHits'),
        HGCHEFConfig = cms.PSet(
            adcNbits = cms.uint32(10),
            adcSaturation = cms.double(100),
            fCPerMIP = cms.vdouble(2.06, 3.43, 5.15),
            isSiFE = cms.bool(True),
            tdcNbits = cms.uint32(12),
            tdcOnset = cms.double(60),
            tdcSaturation = cms.double(10000),
            toaLSB_ns = cms.double(0.0244)
        ),
        HGCHEFdigiCollection = cms.InputTag("hgcalDigis","HEfront"),
        HGCHEFhitCollection = cms.string('HGCHEFUncalibRecHits'),
        HGCHFNoseConfig = cms.PSet(
            adcNbits = cms.uint32(10),
            adcSaturation = cms.double(100),
            fCPerMIP = cms.vdouble(1.25, 2.57, 3.88),
            isSiFE = cms.bool(False),
            tdcNbits = cms.uint32(12),
            tdcOnset = cms.double(60),
            tdcSaturation = cms.double(10000),
            toaLSB_ns = cms.double(0.0244)
        ),
        HGCHFNosedigiCollection = cms.InputTag("hfnoseDigis","HFNose"),
        HGCHFNosehitCollection = cms.string('HGCHFNoseUncalibRecHits'),
        algo = cms.string('HGCalUncalibRecHitWorkerWeights')
    )

    process.HGCalRecHit = cms.EDProducer("HGCalRecHitProducer",
        HGCEE_cce = cms.PSet(
            refToPSet_ = cms.string('HGCAL_chargeCollectionEfficiencies')
        ),
        HGCEE_fCPerMIP = cms.vdouble(2.06, 3.43, 5.15),
        HGCEE_isSiFE = cms.bool(True),
        HGCEE_keV2DIGI = cms.double(0.044259),
        HGCEE_noise_fC = cms.PSet(
            refToPSet_ = cms.string('HGCAL_noise_fC')
        ),
        HGCEErechitCollection = cms.string('HGCEERecHits'),
        HGCEEuncalibRecHitCollection = cms.InputTag("HGCalUncalibRecHit","HGCEEUncalibRecHits"),
        HGCHEB_isSiFE = cms.bool(True),
        HGCHEB_keV2DIGI = cms.double(0.00148148148148),
        HGCHEB_noise_MIP = cms.PSet(
            refToPSet_ = cms.string('HGCAL_noise_heback')
        ),
        HGCHEBrechitCollection = cms.string('HGCHEBRecHits'),
        HGCHEBuncalibRecHitCollection = cms.InputTag("HGCalUncalibRecHit","HGCHEBUncalibRecHits"),
        HGCHEF_cce = cms.PSet(
            refToPSet_ = cms.string('HGCAL_chargeCollectionEfficiencies')
        ),
        HGCHEF_fCPerMIP = cms.vdouble(2.06, 3.43, 5.15),
        HGCHEF_isSiFE = cms.bool(True),
        HGCHEF_keV2DIGI = cms.double(0.044259),
        HGCHEF_noise_fC = cms.PSet(
            refToPSet_ = cms.string('HGCAL_noise_fC')
        ),
        HGCHEFrechitCollection = cms.string('HGCHEFRecHits'),
        HGCHEFuncalibRecHitCollection = cms.InputTag("HGCalUncalibRecHit","HGCHEFUncalibRecHits"),
        HGCHFNose_cce = cms.PSet(
            refToPSet_ = cms.string('HGCAL_chargeCollectionEfficiencies')
        ),
        HGCHFNose_fCPerMIP = cms.vdouble(1.25, 2.57, 3.88),
        HGCHFNose_isSiFE = cms.bool(False),
        HGCHFNose_keV2DIGI = cms.double(0.044259),
        HGCHFNose_noise_fC = cms.PSet(
            refToPSet_ = cms.string('HGCAL_noise_fC')
        ),
        HGCHFNoserechitCollection = cms.string('HGCHFNoseRecHits'),
        HGCHFNoseuncalibRecHitCollection = cms.InputTag("HGCalUncalibRecHit","HGCHFNoseUncalibRecHits"),
        algo = cms.string('HGCalRecHitWorkerSimple'),
        constSiPar = cms.double(0.02),
        layerNoseWeights = cms.vdouble(
            0.0, 39.500245, 39.756638, 39.756638, 39.756638,
            39.756638, 66.020266, 92.283895, 92.283895
        ),
        layerWeights = cms.vdouble(
            0.0, 8.894541, 10.937907, 10.937907, 10.937907,
            10.937907, 10.937907, 10.937907, 10.937907, 10.937907,
            10.932882, 10.932882, 10.937907, 10.937907, 10.938169,
            10.938169, 10.938169, 10.938169, 10.938169, 10.938169,
            10.938169, 10.938169, 10.938169, 10.938169, 10.938169,
            10.938169, 10.938169, 10.938169, 32.332097, 51.574301,
            51.444192, 51.444192, 51.444192, 51.444192, 51.444192,
            51.444192, 51.444192, 51.444192, 51.444192, 51.444192,
            69.513118, 87.582044, 87.582044, 87.582044, 87.582044,
            87.582044, 87.214571, 86.888309, 86.92952, 86.92952,
            86.92952
        ),
        maxValSiPar = cms.double(10000.0),
        minValSiPar = cms.double(10.0),
        noiseSiPar = cms.double(5.5),
        rangeMask = cms.uint32(4294442496),
        rangeMatch = cms.uint32(1161838592),
        thicknessCorrection = cms.vdouble(1.132,1.092,1.084, 1.0, 1.0, 1.0), # 100, 200, 300 um
        deltasi_index_regemfac = cms.int32(3),
        sciThicknessCorrection = cms.double(1.0),
        thicknessNoseCorrection = cms.vdouble(1.132,1.092,1.084), # 100, 200, 300 um
    )


    process.hgcalLayerClusters = cms.EDProducer("HGCalLayerClusterProducer",
        HFNoseInput = cms.InputTag("HGCalRecHit","HGCHFNoseRecHits"),
        HGCBHInput = cms.InputTag("HGCalRecHit","HGCHEBRecHits"),
        HGCEEInput = cms.InputTag("HGCalRecHit","HGCEERecHits"),
        HGCFHInput = cms.InputTag("HGCalRecHit","HGCHEFRecHits"),
        detector = cms.string('all'),
        doSharing = cms.bool(False),
        mightGet = cms.optional.untracked.vstring,
        nHitsTime = cms.uint32(3),
        plugin = cms.PSet(
            dEdXweights = cms.vdouble(
                0.0, 8.894541, 10.937907, 10.937907, 10.937907,
                10.937907, 10.937907, 10.937907, 10.937907, 10.937907,
                10.932882, 10.932882, 10.937907, 10.937907, 10.938169,
                10.938169, 10.938169, 10.938169, 10.938169, 10.938169,
                10.938169, 10.938169, 10.938169, 10.938169, 10.938169,
                10.938169, 10.938169, 10.938169, 32.332097, 51.574301,
                51.444192, 51.444192, 51.444192, 51.444192, 51.444192,
                51.444192, 51.444192, 51.444192, 51.444192, 51.444192,
                69.513118, 87.582044, 87.582044, 87.582044, 87.582044,
                87.582044, 87.214571, 86.888309, 86.92952, 86.92952,
                86.92952
            ),
            deltac = cms.vdouble(1.3, 1.3, 5, 0.0315),
            dependSensor = cms.bool(True),
            ecut = cms.double(3),
            fcPerEle = cms.double(0.00016020506),
            fcPerMip = cms.vdouble(2.06, 3.43, 5.15),
            kappa = cms.double(9),
            noiseMip = cms.PSet(
                refToPSet_ = cms.string('HGCAL_noise_heback')
            ),
            noises = cms.PSet(
                refToPSet_ = cms.string('HGCAL_noises')
            ),
            thicknessCorrection = cms.vdouble(0.781, 0.775, 0.769),
            thresholdW0 = cms.vdouble(2.9, 2.9, 2.9),
            type = cms.string('CLUE'),
            use2x2 = cms.bool(True),
            verbosity = cms.untracked.uint32(3)
        ),
        timeClname = cms.string('timeLayerCluster'),
        timeOffset = cms.double(5)
    )

    process.filteredLayerClustersMIP = cms.EDProducer("FilteredLayerClustersProducer",
        HGCLayerClusters = cms.InputTag("hgcalLayerClusters"),
        LayerClustersInputMask = cms.InputTag("hgcalLayerClusters","InitialLayerClustersMask"),
        algo_number = cms.int32(8),
        clusterFilter = cms.string('ClusterFilterBySize'),
        iteration_label = cms.string('MIP'),
        max_cluster_size = cms.int32(2),
        mightGet = cms.optional.untracked.vstring,
        min_cluster_size = cms.int32(0)
    )

    process.ticlSeedingGlobal = cms.EDProducer("TICLSeedingRegionProducer",
        algoId = cms.int32(2),
        algo_verbosity = cms.int32(0),
        cutTk = cms.string('1.48 < abs(eta) < 3.0 && pt > 2. && quality("highPurity") && hitPattern().numberOfLostHits("MISSING_OUTER_HITS") < 10'),
        mightGet = cms.optional.untracked.vstring,
        propagator = cms.string('PropagatorWithMaterial'),
        tracks = cms.InputTag("")
    )

    process.ticlLayerTileProducer = cms.EDProducer("TICLLayerTileProducer",
        layer_clusters = cms.InputTag("hgcalLayerClusters"),
        mightGet = cms.optional.untracked.vstring
    )

    process.trackstersMIP = cms.EDProducer("TrackstersProducer",
        algo_verbosity = cms.int32(0),
        eid_graph_path = cms.string('RecoHGCal/TICL/data/tf_models/energy_id_v0.pb'),
        eid_input_name = cms.string('input'),
        eid_min_cluster_energy = cms.double(1),
        eid_n_clusters = cms.int32(10),
        eid_n_layers = cms.int32(50),
        eid_output_name_energy = cms.string('output/regressed_energy'),
        eid_output_name_id = cms.string('output/id_probabilities'),
        filtered_mask = cms.InputTag("filteredLayerClustersMIP","MIP"),
        layer_clusters = cms.InputTag("hgcalLayerClusters"),
        layer_clusters_tiles = cms.InputTag("ticlLayerTileProducer"),
        max_delta_time = cms.double(3),
        max_out_in_hops = cms.int32(10),
        mightGet = cms.optional.untracked.vstring,
        min_clusters_per_ntuplet = cms.int32(15),
        min_cos_pointing = cms.double(0.9),
        min_cos_theta = cms.double(0.99),
        missing_layers = cms.int32(3),
        original_mask = cms.InputTag("hgcalLayerClusters","InitialLayerClustersMask"),
        out_in_dfs = cms.bool(False),
        seeding_regions = cms.InputTag("ticlSeedingGlobal"),
        time_layerclusters = cms.InputTag("hgcalLayerClusters","timeLayerCluster")
    )


    process.particleFlowRecHitHGC = cms.EDProducer("PFRecHitProducer",
        navigator = cms.PSet(
            hgcee = cms.PSet(
                name = cms.string('PFRecHitHGCEENavigator'),
                topologySource = cms.string('HGCalEESensitive')
            ),
            hgcheb = cms.PSet(
                name = cms.string('PFRecHitHGCHENavigator'),
                topologySource = cms.string('HGCalHEScintillatorSensitive')
            ),
            hgchef = cms.PSet(
                name = cms.string('PFRecHitHGCHENavigator'),
                topologySource = cms.string('HGCalHESiliconSensitive')
            ),
            name = cms.string('PFRecHitHGCNavigator')
        ),
        producers = cms.VPSet(
            cms.PSet(
                geometryInstance = cms.string('HGCalEESensitive'),
                name = cms.string('PFHGCalEERecHitCreator'),
                qualityTests = cms.VPSet(cms.PSet(
                    name = cms.string('PFRecHitQTestHGCalThresholdSNR'),
                    thresholdSNR = cms.double(5.0)
                )),
                src = cms.InputTag("HGCalRecHit","HGCEERecHits")
            ),
            cms.PSet(
                geometryInstance = cms.string('HGCalHESiliconSensitive'),
                name = cms.string('PFHGCalHSiRecHitCreator'),
                qualityTests = cms.VPSet(cms.PSet(
                    name = cms.string('PFRecHitQTestHGCalThresholdSNR'),
                    thresholdSNR = cms.double(5.0)
                )),
                src = cms.InputTag("HGCalRecHit","HGCHEFRecHits")
            ),
            cms.PSet(
                geometryInstance = cms.string(''),
                name = cms.string('PFHGCalHScRecHitCreator'),
                qualityTests = cms.VPSet(cms.PSet(
                    name = cms.string('PFRecHitQTestHGCalThresholdSNR'),
                    thresholdSNR = cms.double(5.0)
                )),
                src = cms.InputTag("HGCalRecHit","HGCHEBRecHits")
            )
        )
    )
    process.filteredLayerClusters = cms.EDProducer("FilteredLayerClustersProducer",
        HGCLayerClusters = cms.InputTag("hgcalLayerClusters"),
        LayerClustersInputMask = cms.InputTag("trackstersMIP"),
        algo_number = cms.int32(8),
        clusterFilter = cms.string('ClusterFilterByAlgoAndSize'),
        iteration_label = cms.string('algo8'),
        max_cluster_size = cms.int32(9999),
        mightGet = cms.optional.untracked.vstring,
        min_cluster_size = cms.int32(2)
    )

    process.trackstersEM = cms.EDProducer("TrackstersProducer",
        algo_verbosity = cms.int32(0),
        eid_graph_path = cms.string('RecoHGCal/TICL/data/tf_models/energy_id_v0.pb'),
        eid_input_name = cms.string('input'),
        eid_min_cluster_energy = cms.double(1),
        eid_n_clusters = cms.int32(10),
        eid_n_layers = cms.int32(50),
        eid_output_name_energy = cms.string('output/regressed_energy'),
        eid_output_name_id = cms.string('output/id_probabilities'),
        filtered_mask = cms.InputTag("filteredLayerClusters","algo8"),
        layer_clusters = cms.InputTag("hgcalLayerClusters"),
        layer_clusters_tiles = cms.InputTag("ticlLayerTileProducer"),
        max_delta_time = cms.double(3),
        max_out_in_hops = cms.int32(4),
        mightGet = cms.optional.untracked.vstring,
        min_clusters_per_ntuplet = cms.int32(10),
        min_cos_pointing = cms.double(0.9),
        min_cos_theta = cms.double(0.984),
        missing_layers = cms.int32(1),
        original_mask = cms.InputTag("trackstersMIP"),
        out_in_dfs = cms.bool(True),
        seeding_regions = cms.InputTag("ticlSeedingGlobal"),
        time_layerclusters = cms.InputTag("hgcalLayerClusters","timeLayerCluster")
    )

    process.multiClustersFromTrackstersEM = cms.EDProducer("MultiClustersFromTrackstersProducer",
        LayerClusters = cms.InputTag("hgcalLayerClusters"),
        Tracksters = cms.InputTag("trackstersEM"),
        mightGet = cms.optional.untracked.vstring,
        verbosity = cms.untracked.uint32(3)
    )

    process.particleFlowClusterHGCalFromTICL = cms.EDProducer("PFClusterProducer",
        energyCorrector = cms.PSet(

        ),
        initialClusteringStep = cms.PSet(
            algoName = cms.string('PFClusterFromHGCalMultiCluster'),
            clusterSrc = cms.InputTag("multiClustersFromTrackstersEM"),
            thresholdsByDetector = cms.VPSet()
        ),
        pfClusterBuilder = cms.PSet(

        ),
        positionReCalc = cms.PSet(
            algoName = cms.string('Cluster3DPCACalculator'),
            minFractionInCalc = cms.double(1e-09),
            updateTiming = cms.bool(False)
        ),
        recHitCleaners = cms.VPSet(),
        recHitsSource = cms.InputTag("particleFlowRecHitHGC"),
        seedCleaners = cms.VPSet(),
        seedFinder = cms.PSet(
            algoName = cms.string('PassThruSeedFinder'),
            nNeighbours = cms.int32(8),
            thresholdsByDetector = cms.VPSet()
        )
    )

    process.offlineBeamSpot = cms.EDProducer("BeamSpotProducer")

    process.particleFlowSuperClusterHGCalFromTICL = cms.EDProducer("PFECALSuperClusterProducer",
        BeamSpot = cms.InputTag("hltOnlineBeamSpot"),
        ClusteringType = cms.string('Mustache'),
        ESAssociation = cms.InputTag("hltParticleFlowClusterECALUnseeded"),
        EnergyWeight = cms.string('Raw'),
        PFBasicClusterCollectionBarrel = cms.string('particleFlowBasicClusterECALBarrel'),
        PFBasicClusterCollectionEndcap = cms.string(''),
        PFBasicClusterCollectionPreshower = cms.string('particleFlowBasicClusterECALPreshower'),
        PFClusters = cms.InputTag("particleFlowClusterHGCalFromTICL"),
        PFSuperClusterCollectionBarrel = cms.string('particleFlowSuperClusterECALBarrel'),
        PFSuperClusterCollectionEndcap = cms.string(''),
        PFSuperClusterCollectionEndcapWithPreshower = cms.string(''),
        applyCrackCorrections = cms.bool(False),
        doSatelliteClusterMerge = cms.bool(False),
        dropUnseedable = cms.bool(True),
        etawidth_SuperClusterBarrel = cms.double(0.04),
        etawidth_SuperClusterEndcap = cms.double(0.04),
        phiwidth_SuperClusterBarrel = cms.double(0.6),
        phiwidth_SuperClusterEndcap = cms.double(0.6),
        regressionConfig = cms.PSet(
            applySigmaIetaIphiBug = cms.bool(False),
            ecalRecHitsEB = cms.InputTag("hltEcalRecHit","EcalRecHitsEB"),
            ecalRecHitsEE = cms.InputTag("hltEcalRecHit","EcalRecHitsEE"),
            isHLT = cms.bool(True),
            regressionKeyEB = cms.string('pfscecal_EBCorrection_offline_v2'),
            regressionKeyEE = cms.string('pfscecal_EECorrection_offline_v2'),
            uncertaintyKeyEB = cms.string('pfscecal_EBUncertainty_offline_v2'),
            uncertaintyKeyEE = cms.string('pfscecal_EEUncertainty_offline_v2'),
            vertexCollection = cms.InputTag("offlinePrimaryVertices")
        ),
        satelliteClusterSeedThreshold = cms.double(50.0),
        satelliteMajorityFraction = cms.double(0.5),
        seedThresholdIsET = cms.bool(True),
        thresh_PFClusterBarrel = cms.double(0.0),
        thresh_PFClusterES = cms.double(0.0),
        thresh_PFClusterEndcap = cms.double(0.15),
        thresh_PFClusterSeedBarrel = cms.double(1.0),
        thresh_PFClusterSeedEndcap = cms.double(1.0),
        thresh_SCEt = cms.double(4.0),
        useDynamicDPhiWindow = cms.bool(True),
        useRegression = cms.bool(False),
        use_preshower = cms.bool(False),
        verbose = cms.untracked.bool(False)
    )

    process.hltMuonHgcalPFClusterIsoForMuons = cms.EDProducer("MuonHLTEcalPFClusterIsolationProducer",
        absEtaLowEdges = cms.vdouble(0.0, 1.479),
        doRhoCorrection = cms.bool(True),
        drMax = cms.double(0.3),
        drVetoBarrel = cms.double(0.05),
        drVetoEndcap = cms.double(0.05),
        effectiveAreas = cms.vdouble(0.29, 0.21),
        energyBarrel = cms.double(0.0),
        energyEndcap = cms.double(0.0),
        etaStripBarrel = cms.double(0.0),
        etaStripEndcap = cms.double(0.0),
        pfClusterProducer = cms.InputTag("particleFlowClusterHGCalFromTICL"),
        recoCandidateProducer = cms.InputTag("hltIterL3MuonCandidates"),
        rhoMax = cms.double(99999999.0),
        rhoProducer = cms.InputTag("hltFixedGridRhoFastjetECALMFForMuons"),
        rhoScale = cms.double(1.0)
    )


    process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhgcalIsoRhoFilteredHGB0p14HGE0p10 = cms.EDFilter("HLTMuonGenericFilter",
        absEtaLowEdges = cms.vdouble(0.0, 1.479),
        candTag = cms.InputTag("hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFilteredHB0p16HE0p20"),
        doRhoCorrection = cms.bool(False),
        effectiveAreas = cms.vdouble(0.0, 0.0),
        energyLowEdges = cms.vdouble(0.0),
        l1EGCand = cms.InputTag("hltIterL3MuonCandidates"),
        lessThan = cms.bool(True),
        ncandcut = cms.int32(1),
        rhoMax = cms.double(99999999.0),
        rhoScale = cms.double(1.0),
        rhoTag = cms.InputTag(""),
        saveTags = cms.bool(True),
        thrOverE2EB = cms.vdouble(-1.0),
        thrOverE2EE = cms.vdouble(-1.0),
        thrOverEEB = cms.vdouble(0.14),
        thrOverEEE = cms.vdouble(0.1),
        thrRegularEB = cms.vdouble(-1.0),
        thrRegularEE = cms.vdouble(-1.0),
        useEt = cms.bool(True),
        varTag = cms.InputTag("hltMuonHgcalPFClusterIsoForMuons")
    )

    process.HLTL3muonHgcalPFisorecoSequenceNoBoolsForMuons = cms.Sequence(
       process.hgcalDigis +
       process.HGCalUncalibRecHit +
       process.HGCalRecHit +
       process.hgcalLayerClusters +
       process.filteredLayerClustersMIP +
       process.ticlSeedingGlobal +
       process.ticlLayerTileProducer +
       process.trackstersMIP +
       process.particleFlowRecHitHGC +
       process.filteredLayerClusters +
       process.trackstersEM +
       process.multiClustersFromTrackstersEM +
       process.particleFlowClusterHGCalFromTICL +
       process.offlineBeamSpot +
       #process.particleFlowSuperClusterHGCalFromTICL +
       process.hltMuonHgcalPFClusterIsoForMuons
    )

    #######################################
    ### processes for Track-based Isolation
    #######################################
    process.hltL3MuonVertex = cms.EDProducer( "VertexFromTrackProducer",
        verbose = cms.untracked.bool( False ),
        useTriggerFilterElectrons = cms.bool( False ),
        beamSpotLabel = cms.InputTag( "hltOnlineBeamSpot" ),
        isRecoCandidate = cms.bool( True ),
        trackLabel = cms.InputTag( "hltIterL3MuonCandidates" ),
        useTriggerFilterMuons = cms.bool( False ),
        useBeamSpot = cms.bool( True ),
        vertexLabel = cms.InputTag( "notUsed" ),
        triggerFilterElectronsSrc = cms.InputTag( "notUsed" ),
        triggerFilterMuonsSrc = cms.InputTag( "notUsed" ),
        useVertex = cms.bool( False )
    )

    ##### check how many layers we actually need!!!!
    process.hltPixelLayerQuadruplets = cms.EDProducer("SeedingLayersEDProducer",
        BPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        FPix = cms.PSet(
            HitProducer = cms.string('hltSiPixelRecHits'),
            TTRHBuilder = cms.string('WithTrackAngle')
        ),
        MTEC = cms.PSet(

        ),
        MTIB = cms.PSet(

        ),
        MTID = cms.PSet(

        ),
        MTOB = cms.PSet(

        ),
        TEC = cms.PSet(

        ),
        TIB = cms.PSet(

        ),
        TID = cms.PSet(

        ),
        TOB = cms.PSet(

        ),
        layerList = cms.vstring(
            'BPix1+BPix2+BPix3+BPix4', 
            'BPix1+BPix2+BPix3+FPix1_pos', 
            'BPix1+BPix2+BPix3+FPix1_neg', 
            'BPix1+BPix2+FPix1_pos+FPix2_pos', 
            'BPix1+BPix2+FPix1_neg+FPix2_neg', 
            'BPix1+FPix1_pos+FPix2_pos+FPix3_pos', 
            'BPix1+FPix1_neg+FPix2_neg+FPix3_neg', 
            'FPix1_pos+FPix2_pos+FPix3_pos+FPix4_pos', 
            'FPix1_neg+FPix2_neg+FPix3_neg+FPix4_neg', 
            'FPix2_pos+FPix3_pos+FPix4_pos+FPix5_pos', 
            'FPix2_neg+FPix3_neg+FPix4_neg+FPix5_neg', 
            'FPix3_pos+FPix4_pos+FPix5_pos+FPix6_pos', 
            'FPix3_neg+FPix4_neg+FPix5_neg+FPix6_neg', 
            'FPix4_pos+FPix5_pos+FPix6_pos+FPix7_pos', 
            'FPix4_neg+FPix5_neg+FPix6_neg+FPix7_neg', 
            'FPix5_pos+FPix6_pos+FPix7_pos+FPix8_pos', 
            'FPix5_neg+FPix6_neg+FPix7_neg+FPix8_neg'
        )
    )

    process.hltPixelTracksL3MuonFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
        chi2 = cms.double( 1000.0 ),
        nSigmaTipMaxTolerance = cms.double( 0.0 ),
        ptMin = cms.double( 0.9 ), ##before it was 0.1
        nSigmaInvPtTolerance = cms.double( 0.0 ),
        tipMax = cms.double( 1.0 )
    )
    process.hltPixelTracksL3MuonFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool( False ),
        scaleFactor = cms.double( 0.65 )
    )

    process.hltPixelTracksTrackingRegionsL3Muon = cms.EDProducer( "GlobalTrackingRegionWithVerticesEDProducer",
        RegionPSet = cms.PSet( 
          useFixedError = cms.bool( True ),
          nSigmaZ = cms.double( 4.0 ),
          VertexCollection = cms.InputTag( "hltL3MuonVertex" ),
          beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
          useFoundVertices = cms.bool( True ),
          fixedError = cms.double( 0.5 ),
          sigmaZVertex = cms.double( 4.0 ),
          useFakeVertices = cms.bool( True ),
          ptMin = cms.double( 0.9 ),
          originRadius = cms.double( 0.2 ),
          precise = cms.bool( True ),
          useMultipleScattering = cms.bool( False )
        )
    )
    process.hltPixelTracksHitDoubletsL3Muon = cms.EDProducer( "HitPairEDProducer",
        trackingRegions = cms.InputTag( "hltPixelTracksTrackingRegionsL3Muon" ),
        layerPairs = cms.vuint32( 0, 1, 2 ),
        clusterCheck = cms.InputTag( "" ),
        produceSeedingHitSets = cms.bool( False ),
        produceIntermediateHitDoublets = cms.bool( True ),
        trackingRegionsSeedingLayers = cms.InputTag( "" ),
        maxElement = cms.uint32( 0 ),
        seedingLayers = cms.InputTag( "hltPixelLayerQuadruplets" )
    )
    process.hltPixelTracksHitQuadrupletsL3Muon = cms.EDProducer( "CAHitQuadrupletEDProducer",
        CAThetaCut = cms.double( 0.002 ),
        SeedComparitorPSet = cms.PSet( 
          clusterShapeHitFilter = cms.string( "ClusterShapeHitFilter" ),
          ComponentName = cms.string( "LowPtClusterShapeSeedComparitor" ),
          clusterShapeCacheSrc = cms.InputTag( "hltSiPixelClustersCache" )
        ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        doublets = cms.InputTag( "hltPixelTracksHitDoubletsL3Muon" ),
        fitFastCircle = cms.bool( True ),
        CAHardPtCut = cms.double( 0.0 ),
        maxChi2 = cms.PSet( 
          value2 = cms.double( 50.0 ),
          value1 = cms.double( 200.0 ),
          pt1 = cms.double( 0.7 ),
          enabled = cms.bool( True ),
          pt2 = cms.double( 2.0 )
        ),
        CAPhiCut = cms.double( 0.2 ),
        useBendingCorrection = cms.bool( True ),
        fitFastCircleChi2Cut = cms.bool( True )
    )
    process.hltPixelTracksL3Muon = cms.EDProducer( "PixelTrackProducer",
        Filter = cms.InputTag( "hltPixelTracksL3MuonFilter" ),
        Cleaner = cms.string( "hltPixelTracksCleanerBySharedHits" ),
        passLabel = cms.string( "" ),
        Fitter = cms.InputTag( "hltPixelTracksL3MuonFitter" ),
        SeedingHitSets = cms.InputTag( "hltPixelTracksHitQuadrupletsL3Muon" )
    )

    process.hltPixelVerticesL3Muon = cms.EDProducer( "PixelVertexProducer",
        WtAverage = cms.bool( True ),
        Method2 = cms.bool( True ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        PVcomparer = cms.PSet(  refToPSet_ = cms.string( "hltPhase2PSetPvClusterComparerForIT" ) ),
        Verbosity = cms.int32( 0 ),
        UseError = cms.bool( True ),
        TrackCollection = cms.InputTag( "hltPixelTracksL3Muon" ),
        PtMin = cms.double( 1.0 ),
        NTrkMin = cms.int32( 2 ),
        ZOffset = cms.double( 5.0 ),
        Finder = cms.string( "DivisiveVertexFinder" ),
        ZSeparation = cms.double( 0.05 )
    )

    process.HLTPixelTrackingL3Muon = cms.Sequence( process.hltL3MuonVertex +
                                                   process.HLTDoLocalPixelSequence + 
                                                   process.hltPixelLayerQuadruplets + 
                                                   process.hltPixelTracksL3MuonFilter +
                                                   process.hltPixelTracksL3MuonFitter + 
                                                   process.hltPixelTracksTrackingRegionsL3Muon + 
                                                   process.hltPixelTracksHitDoubletsL3Muon + 
                                                   process.hltPixelTracksHitQuadrupletsL3Muon + 
                                                   process.hltPixelTracksL3Muon + 
                                                   process.hltPixelVerticesL3Muon )



    process.hltPixelTracksForSeedsL3MuonFilter = cms.EDProducer( "PixelTrackFilterByKinematicsProducer",
        chi2 = cms.double( 1000.0 ),
        nSigmaTipMaxTolerance = cms.double( 0.0 ),
        ptMin = cms.double( 0.9 ), 
        nSigmaInvPtTolerance = cms.double( 0.0 ),
        tipMax = cms.double( 1.0 )
    )
    process.hltPixelTracksForSeedsL3MuonFitter = cms.EDProducer( "PixelFitterByHelixProjectionsProducer",
        scaleErrorsForBPix1 = cms.bool( False ),
        scaleFactor = cms.double( 0.65 )
    )
    process.hltPixelTracksTrackingRegionsForSeedsL3Muon = cms.EDProducer( "CandidateSeededTrackingRegionsEDProducer",
        RegionPSet = cms.PSet( 
          vertexCollection = cms.InputTag( "hltPixelVerticesL3Muon" ),
          zErrorVetex = cms.double( 0.2 ),
          beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
          zErrorBeamSpot = cms.double( 24.2 ),
          maxNVertices = cms.int32( 1 ),
          maxNRegions = cms.int32( 10 ),
          nSigmaZVertex = cms.double( 3.0 ),
          nSigmaZBeamSpot = cms.double( 4.0 ),
          ptMin = cms.double( 0.9 ),
          mode = cms.string( "VerticesFixed" ),
          input = cms.InputTag( "hltIterL3MuonCandidates" ),
          searchOpt = cms.bool( False ),
          whereToUseMeasurementTracker = cms.string( "Never" ),
          originRadius = cms.double( 0.1 ),
          measurementTrackerName = cms.InputTag( "" ),
          precise = cms.bool( True ),
          deltaEta = cms.double( 0.3 ),
          deltaPhi = cms.double( 0.3 )
        )
    )
    process.hltPixelTracksHitDoubletsForSeedsL3Muon = cms.EDProducer( "HitPairEDProducer",
        trackingRegions = cms.InputTag( "hltPixelTracksTrackingRegionsForSeedsL3Muon" ),
        layerPairs = cms.vuint32( 0, 1, 2 ),
        clusterCheck = cms.InputTag( "" ),
        produceSeedingHitSets = cms.bool( False ),
        produceIntermediateHitDoublets = cms.bool( True ),
        trackingRegionsSeedingLayers = cms.InputTag( "" ),
        maxElement = cms.uint32( 0 ),
        seedingLayers = cms.InputTag( "hltPixelLayerQuadruplets" )
    )
    process.hltPixelTracksHitQuadrupletsForSeedsL3Muon = cms.EDProducer( "CAHitQuadrupletEDProducer",
        CAThetaCut = cms.double( 0.002 ),
        SeedComparitorPSet = cms.PSet( 
          clusterShapeHitFilter = cms.string( "ClusterShapeHitFilter" ),
          ComponentName = cms.string( "LowPtClusterShapeSeedComparitor" ),
          clusterShapeCacheSrc = cms.InputTag( "hltSiPixelClustersCache" )
        ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        doublets = cms.InputTag( "hltPixelTracksHitDoubletsForSeedsL3Muon" ),
        fitFastCircle = cms.bool( True ),
        CAHardPtCut = cms.double( 0.0 ),
        maxChi2 = cms.PSet( 
          value2 = cms.double( 50.0 ),
          value1 = cms.double( 200.0 ),
          pt1 = cms.double( 0.7 ),
          enabled = cms.bool( True ),
          pt2 = cms.double( 2.0 )
        ),
        CAPhiCut = cms.double( 0.2 ),
        useBendingCorrection = cms.bool( True ),
        fitFastCircleChi2Cut = cms.bool( True )
    )
    process.hltPixelTracksForSeedsL3Muon = cms.EDProducer( "PixelTrackProducer",
        Filter = cms.InputTag( "hltPixelTracksForSeedsL3MuonFilter" ),
        Cleaner = cms.string( "hltPixelTracksCleanerBySharedHits" ),
        passLabel = cms.string( "" ),
        Fitter = cms.InputTag( "hltPixelTracksForSeedsL3MuonFitter" ),
        SeedingHitSets = cms.InputTag( "hltPixelTracksHitQuadrupletsForSeedsL3Muon" )
    )
    process.hltIter0L3MuonPixelSeedsFromPixelTracks = cms.EDProducer( "SeedGeneratorFromProtoTracksEDProducer",
        useEventsWithNoVertex = cms.bool( True ),
        originHalfLength = cms.double( 0.2 ),
        useProtoTrackKinematics = cms.bool( False ),
        usePV = cms.bool( False ),
        SeedCreatorPSet = cms.PSet(  refToPSet_ = cms.string( "hltPhase2SeedFromProtoTracks" ) ),
        InputVertexCollection = cms.InputTag( "hltPixelVerticesL3Muon" ),
        TTRHBuilder = cms.string( "WithTrackAngle" ),
        InputCollection = cms.InputTag( "hltPixelTracksForSeedsL3Muon" ),
        originRadius = cms.double( 0.1 )
    )
    process.hltIter0L3MuonCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
        src = cms.InputTag( "hltIter0L3MuonPixelSeedsFromPixelTracks" ),
        maxSeedsBeforeCleaning = cms.uint32( 1000 ),
        SimpleMagneticField = cms.string( "ParabolicMf" ),
        TransientInitialStateEstimatorParameters = cms.PSet( 
          propagatorAlongTISE = cms.string( "PropagatorWithMaterialParabolicMf" ),
          numberMeasurementsForFit = cms.int32( 4 ),
          propagatorOppositeTISE = cms.string( "PropagatorWithMaterialParabolicMfOpposite" )
        ),
        TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" ),
        cleanTrajectoryAfterInOut = cms.bool( False ),
        useHitsSplitting = cms.bool( False ),
        RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
        doSeedingRegionRebuilding = cms.bool( False ),
        maxNSeeds = cms.uint32( 100000 ),
        TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter0GroupedCkfTrajectoryBuilderIT" ) ),                                         
        NavigationSchool = cms.string( "SimpleNavigationSchool" ),
        TrajectoryBuilder = cms.string( "" )
    )
    process.hltIter0L3MuonCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
        src = cms.InputTag( "hltIter0L3MuonCkfTrackCandidates" ),
        SimpleMagneticField = cms.string(''),    
        clusterRemovalInfo = cms.InputTag( "" ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        MeasurementTrackerEvent = cms.InputTag( "hltSiStripClusters" ),
        Fitter = cms.string('FlexibleKFFittingSmoother'),
        useHitsSplitting = cms.bool( False ),
        MeasurementTracker = cms.string( "" ),
        AlgorithmName = cms.string( "hltIterX" ),
        alias = cms.untracked.string( "ctfWithMaterialTracks" ),
        NavigationSchool = cms.string( "" ),
        TrajectoryInEvent = cms.bool( False ),
        TTRHBuilder = cms.string( "WithTrackAngle" ),
        GeometricInnerState = cms.bool( True ),
        useSimpleMF = cms.bool(False),
        Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
    )
    process.hltIter0L3MuonTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
        src = cms.InputTag( "hltIter0L3MuonCtfWithMaterialTracks" ),
        beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
        vertices = cms.InputTag( "hltPixelVerticesL3Muon" ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet( 
          minPixelHits = cms.vint32( 0, 3, 4 ),
          maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
          dr_par = cms.PSet( 
            d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
            dr_par2 = cms.vdouble( 0.3, 0.3, 0.3 ),
            dr_par1 = cms.vdouble( 0.4, 0.4, 0.4 ),
            dr_exp = cms.vint32( 4, 4, 4 ),
            d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
          ),
          maxLostLayers = cms.vint32( 1, 1, 1 ),
          min3DLayers = cms.vint32( 0, 3, 4 ),
          dz_par = cms.PSet( 
            dz_par1 = cms.vdouble( 0.4, 0.4, 0.4 ),
            dz_par2 = cms.vdouble( 0.35, 0.35, 0.35 ),
            dz_exp = cms.vint32( 4, 4, 4 )
          ),
          minNVtxTrk = cms.int32( 3 ),
          maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ),
          minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ),
          maxChi2 = cms.vdouble( 9999.0, 25.0, 16.0 ),
          maxChi2n = cms.vdouble( 1.2, 1.0, 0.7 ),
          maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ),
          minLayers = cms.vint32( 3, 3, 4 )
        ),
        ignoreVertices = cms.bool( False )
    )
    process.hltIter0L3MuonTrackSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
        minQuality = cms.string( "highPurity" ),
        copyExtras = cms.untracked.bool( True ),
        copyTrajectories = cms.untracked.bool( False ),
        originalSource = cms.InputTag( "hltIter0L3MuonCtfWithMaterialTracks" ),
        originalQualVals = cms.InputTag( 'hltIter0L3MuonTrackCutClassifier','QualityMasks' ),
        originalMVAVals = cms.InputTag( 'hltIter0L3MuonTrackCutClassifier','MVAValues' )
    )

    process.HLTIterativeTrackingL3MuonIteration0 = cms.Sequence( process.hltPixelTracksForSeedsL3MuonFilter + process.hltPixelTracksForSeedsL3MuonFitter + process.hltPixelTracksTrackingRegionsForSeedsL3Muon + process.hltPixelTracksHitDoubletsForSeedsL3Muon + process.hltPixelTracksHitQuadrupletsForSeedsL3Muon + process.hltPixelTracksForSeedsL3Muon + process.hltIter0L3MuonPixelSeedsFromPixelTracks + process.hltIter0L3MuonCkfTrackCandidates + process.hltIter0L3MuonCtfWithMaterialTracks + process.hltIter0L3MuonTrackCutClassifier + process.hltIter0L3MuonTrackSelectionHighPurity )


    process.hltIter2L3MuonClustersRefRemoval = cms.EDProducer("TrackClusterRemoverPhase2",
        trackClassifier = cms.InputTag( '','QualityMasks' ),
        minNumberOfLayersWithMeasBeforeFiltering = cms.int32( 0 ),
        maxChi2 = cms.double( 16.0 ),
        trajectories = cms.InputTag("hltIter0IterL3MuonTrackSelectionHighPurity"),
        oldClusterRemovalInfo = cms.InputTag( "" ),
        phase2OTClusters = cms.InputTag( "siPhase2Clusters" ),
        overrideTrkQuals = cms.InputTag( "" ),
        phase2pixelClusters = cms.InputTag( "hltSiPixelClusters" ),
        TrackQuality = cms.string( "highPurity" )
    )
    process.hltIter2L3MuonMaskedMeasurementTrackerEvent = cms.EDProducer( "MaskedMeasurementTrackerEventProducer",
        phase2clustersToSkip = cms.InputTag( "hltIter2L3MuonClustersRefRemoval" ),
        OnDemand = cms.bool( False ),
        src = cms.InputTag( "hltSiStripClusters" )
    )
    process.hltIter2L3MuonPixelLayerTriplets = cms.EDProducer( "SeedingLayersEDProducer",
        layerList = cms.vstring( 'BPix1+BPix2+BPix3',
          'BPix2+BPix3+BPix4',
          'BPix1+BPix3+BPix4',
          'BPix1+BPix2+BPix4',
          'BPix2+BPix3+FPix1_pos',
          'BPix2+BPix3+FPix1_neg',
          'BPix1+BPix2+FPix1_pos',
          'BPix1+BPix2+FPix1_neg',
          'BPix2+FPix1_pos+FPix2_pos',
          'BPix2+FPix1_neg+FPix2_neg',
          'BPix1+FPix1_pos+FPix2_pos',
          'BPix1+FPix1_neg+FPix2_neg',
          'FPix1_pos+FPix2_pos+FPix3_pos',
          'FPix1_neg+FPix2_neg+FPix3_neg' ),
        MTOB = cms.PSet(  ),
        TEC = cms.PSet(  ),
        MTID = cms.PSet(  ),
        FPix = cms.PSet( 
          TTRHBuilder = cms.string( "WithTrackAngle" ),
          skipClusters = cms.InputTag( "hltIter2L3MuonClustersRefRemoval" ),
          HitProducer = cms.string( "hltSiPixelRecHits" )
        ),
        MTEC = cms.PSet(  ),
        MTIB = cms.PSet(  ),
        TID = cms.PSet(  ),
        TOB = cms.PSet(  ),
        BPix = cms.PSet( 
          TTRHBuilder = cms.string( "WithTrackAngle" ),
          skipClusters = cms.InputTag( "hltIter2L3MuonClustersRefRemoval" ),
          HitProducer = cms.string( "hltSiPixelRecHits" )
        ),
        TIB = cms.PSet(  )
    )
    process.hltIter2L3MuonPixelTrackingRegions = cms.EDProducer( "CandidateSeededTrackingRegionsEDProducer",
        RegionPSet = cms.PSet( 
          vertexCollection = cms.InputTag( "hltPixelVerticesL3Muon" ),
          zErrorVetex = cms.double( 0.05 ),
          beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
          zErrorBeamSpot = cms.double( 24.2 ),
          maxNVertices = cms.int32( 1 ),
          maxNRegions = cms.int32( 10 ),
          nSigmaZVertex = cms.double( 3.0 ),
          nSigmaZBeamSpot = cms.double( 4.0 ),
          ptMin = cms.double( 0.9 ), ## it was 0.8
          mode = cms.string( "VerticesFixed" ),
          input = cms.InputTag( "hltIterL3MuonCandidates" ),
          searchOpt = cms.bool( False ),
          whereToUseMeasurementTracker = cms.string( "ForSiStrips" ),
          originRadius = cms.double( 0.025 ),
          measurementTrackerName = cms.InputTag( "hltIter2L3MuonMaskedMeasurementTrackerEvent" ),
          precise = cms.bool( True ),
          deltaEta = cms.double( 0.3 ),
          deltaPhi = cms.double( 0.3 )
        )
    )
    process.hltIter2L3MuonPixelClusterCheck = cms.EDProducer( "ClusterCheckerEDProducer",
        cut = cms.string( "" ),
        silentClusterCheck = cms.untracked.bool( False ),
        MaxNumberOfCosmicClusters = cms.uint32( 50000 ),
        PixelClusterCollectionLabel = cms.InputTag( "hltSiPixelClusters" ),
        doClusterCheck = cms.bool( False ),
        MaxNumberOfPixelClusters = cms.uint32( 10000 ),
        ClusterCollectionLabel = cms.InputTag( "hltSiStripClusters" )
    )
    process.hltIter2L3MuonPixelHitDoublets = cms.EDProducer( "HitPairEDProducer",
        trackingRegions = cms.InputTag( "hltIter2L3MuonPixelTrackingRegions" ),
        layerPairs = cms.vuint32( 0, 1 ),
        clusterCheck = cms.InputTag( "hltIter2L3MuonPixelClusterCheck" ),
        produceSeedingHitSets = cms.bool( False ),
        produceIntermediateHitDoublets = cms.bool( True ),
        trackingRegionsSeedingLayers = cms.InputTag( "" ),
        maxElement = cms.uint32( 0 ),
        seedingLayers = cms.InputTag( "hltIter2L3MuonPixelLayerTriplets" )
    )

    process.hltIter2L3MuonPixelHitTriplets = cms.EDProducer( "CAHitTripletEDProducer",
        CAHardPtCut = cms.double( 0.3 ),
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
        extraHitRPhitolerance = cms.double( 0.032 ),
        doublets = cms.InputTag( "hltIter2L3MuonPixelHitDoublets" ),
        CAThetaCut = cms.double( 0.004 ),
        maxChi2 = cms.PSet( 
          value2 = cms.double( 6.0 ),
          value1 = cms.double( 100.0 ),
          pt1 = cms.double( 0.8 ),
          enabled = cms.bool( True ),
          pt2 = cms.double( 8.0 )
        ),
        CAPhiCut = cms.double( 0.1 ),
        useBendingCorrection = cms.bool( True )
    )
    process.hltIter2L3MuonPixelSeeds = cms.EDProducer( "SeedCreatorFromRegionConsecutiveHitsEDProducer",
        SeedComparitorPSet = cms.PSet(  ComponentName = cms.string( "none" ) ),
        forceKinematicWithRegionDirection = cms.bool( False ),
        magneticField = cms.string( "ParabolicMf" ),
        SeedMomentumForBOFF = cms.double( 5.0 ),
        OriginTransverseErrorMultiplier = cms.double( 1.0 ),
        TTRHBuilder = cms.string( "WithTrackAngle" ),
        MinOneOverPtError = cms.double( 1.0 ),
        seedingHitSets = cms.InputTag( "hltIter2L3MuonPixelHitTriplets" ),
        propagator = cms.string( "PropagatorWithMaterialParabolicMf" )
    )
    process.hltIter2L3MuonCkfTrackCandidates = cms.EDProducer( "CkfTrackCandidateMaker",
        src = cms.InputTag( "hltIter2L3MuonPixelSeeds" ),
        maxSeedsBeforeCleaning = cms.uint32( 1000 ),
        SimpleMagneticField = cms.string( "ParabolicMf" ),
        TransientInitialStateEstimatorParameters = cms.PSet( 
          propagatorAlongTISE = cms.string( "PropagatorWithMaterialParabolicMf" ),
          numberMeasurementsForFit = cms.int32( 4 ),
          propagatorOppositeTISE = cms.string( "PropagatorWithMaterialParabolicMfOpposite" )
        ),
        TrajectoryCleaner = cms.string( "hltESPTrajectoryCleanerBySharedHits" ),
        MeasurementTrackerEvent = cms.InputTag( "hltIter2L3MuonMaskedMeasurementTrackerEvent" ),
        cleanTrajectoryAfterInOut = cms.bool( False ),
        useHitsSplitting = cms.bool( False ),
        RedundantSeedCleaner = cms.string( "CachingSeedCleanerBySharedInput" ),
        doSeedingRegionRebuilding = cms.bool( False ),
        maxNSeeds = cms.uint32( 100000 ),
        TrajectoryBuilderPSet = cms.PSet(  refToPSet_ = cms.string( "HLTIter2GroupedCkfTrajectoryBuilderIT" ) ),
        NavigationSchool = cms.string( "SimpleNavigationSchool" ),
        TrajectoryBuilder = cms.string( "" )
    )
    process.hltIter2L3MuonCtfWithMaterialTracks = cms.EDProducer( "TrackProducer",
        src = cms.InputTag( "hltIter2L3MuonCkfTrackCandidates" ),
        SimpleMagneticField = cms.string(''),
        clusterRemovalInfo = cms.InputTag( "" ),
        beamSpot = cms.InputTag( "hltOnlineBeamSpot" ),
        MeasurementTrackerEvent = cms.InputTag( "hltIter2L3MuonMaskedMeasurementTrackerEvent" ),
        Fitter = cms.string( "FlexibleKFFittingSmoother" ),
        useHitsSplitting = cms.bool( False ),
        MeasurementTracker = cms.string( "" ),
        AlgorithmName = cms.string( "hltIterX" ),
        alias = cms.untracked.string( "ctfWithMaterialTracks" ),
        NavigationSchool = cms.string( "" ),
        TrajectoryInEvent = cms.bool( False ),
        TTRHBuilder = cms.string( "WithTrackAngle" ),
        GeometricInnerState = cms.bool( True ),
        useSimpleMF = cms.bool(False),
        Propagator = cms.string( "hltESPRungeKuttaTrackerPropagator" )
    )

    process.hltIter2L3MuonTrackCutClassifier = cms.EDProducer( "TrackCutClassifier",
        src = cms.InputTag( "hltIter2L3MuonCtfWithMaterialTracks" ),
        beamspot = cms.InputTag( "hltOnlineBeamSpot" ),
        vertices = cms.InputTag( "hltPixelVerticesL3Muon" ),
        qualityCuts = cms.vdouble( -0.7, 0.1, 0.7 ),
        mva = cms.PSet( 
          minPixelHits = cms.vint32( 0, 0, 0 ),
          maxDzWrtBS = cms.vdouble( 3.40282346639E38, 24.0, 15.0 ),
          dr_par = cms.PSet( 
            d0err = cms.vdouble( 0.003, 0.003, 0.003 ),
            dr_par2 = cms.vdouble( 3.40282346639E38, 0.3, 0.3 ),
            dr_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
            dr_exp = cms.vint32( 4, 4, 4 ),
            d0err_par = cms.vdouble( 0.001, 0.001, 0.001 )
          ),
          maxLostLayers = cms.vint32( 1, 1, 1 ),
          min3DLayers = cms.vint32( 0, 0, 0 ),
          dz_par = cms.PSet( 
            dz_par1 = cms.vdouble( 3.40282346639E38, 0.4, 0.4 ),
            dz_par2 = cms.vdouble( 3.40282346639E38, 0.35, 0.35 ),
            dz_exp = cms.vint32( 4, 4, 4 )
          ),
          minNVtxTrk = cms.int32( 3 ),
          maxDz = cms.vdouble( 0.5, 0.2, 3.40282346639E38 ),
          minNdof = cms.vdouble( 1.0E-5, 1.0E-5, 1.0E-5 ),
          maxChi2 = cms.vdouble( 9999.0, 25.0, 16.0 ),
          maxChi2n = cms.vdouble( 1.2, 1.0, 0.7 ),
          maxDr = cms.vdouble( 0.5, 0.03, 3.40282346639E38 ),
          minLayers = cms.vint32( 3, 3, 3 )
        ),
        ignoreVertices = cms.bool( False )
    )
    process.hltIter2L3MuonTrackSelectionHighPurity = cms.EDProducer( "TrackCollectionFilterCloner",
        minQuality = cms.string( "highPurity" ),
        copyExtras = cms.untracked.bool( True ),
        copyTrajectories = cms.untracked.bool( False ),
        originalSource = cms.InputTag( "hltIter2L3MuonCtfWithMaterialTracks" ),
        originalQualVals = cms.InputTag( 'hltIter2L3MuonTrackCutClassifier','QualityMasks' ),
        originalMVAVals = cms.InputTag( 'hltIter2L3MuonTrackCutClassifier','MVAValues' )
    )

    process.HLTIterativeTrackingL3MuonIteration2 = cms.Sequence( process.hltIter2L3MuonClustersRefRemoval + process.hltIter2L3MuonMaskedMeasurementTrackerEvent + process.hltIter2L3MuonPixelLayerTriplets + process.hltIter2L3MuonPixelTrackingRegions + process.hltIter2L3MuonPixelClusterCheck + process.hltIter2L3MuonPixelHitDoublets + process.hltIter2L3MuonPixelHitTriplets + process.hltIter2L3MuonPixelSeeds + process.hltIter2L3MuonCkfTrackCandidates + process.hltIter2L3MuonCtfWithMaterialTracks + process.hltIter2L3MuonTrackCutClassifier + process.hltIter2L3MuonTrackSelectionHighPurity )


    process.hltIter2L3MuonMerged = cms.EDProducer( "TrackListMerger",
        ShareFrac = cms.double( 0.19 ),
        writeOnlyTrkQuals = cms.bool( False ),
        MinPT = cms.double( 0.05 ),
        allowFirstHitShare = cms.bool( True ),
        copyExtras = cms.untracked.bool( True ),
        Epsilon = cms.double( -0.001 ),
        #selectedTrackQuals = cms.VInputTag( 'hltIter1L3MuonMerged','hltIter2L3MuonTrackSelectionHighPurity' ),
        selectedTrackQuals = cms.VInputTag( 'hltIter0L3MuonTrackSelectionHighPurity','hltIter2L3MuonTrackSelectionHighPurity' ),
        indivShareFrac = cms.vdouble( 1.0, 1.0 ),
        MaxNormalizedChisq = cms.double( 1000.0 ),
        copyMVA = cms.bool( False ),
        FoundHitBonus = cms.double( 5.0 ),
        LostHitPenalty = cms.double( 20.0 ),
        setsToMerge = cms.VPSet( 
          cms.PSet(  pQual = cms.bool( False ),
            tLists = cms.vint32( 0, 1 )
          )
        ),
        MinFound = cms.int32( 3 ),
        hasSelector = cms.vint32( 0, 0 ),
        #TrackProducers = cms.VInputTag( 'hltIter1L3MuonMerged','hltIter2L3MuonTrackSelectionHighPurity' ),
        TrackProducers = cms.VInputTag( 'hltIter0L3MuonTrackSelectionHighPurity','hltIter2L3MuonTrackSelectionHighPurity' ),
        trackAlgoPriorityOrder = cms.string( "hltESPTrackAlgoPriorityOrder" ),
        newQuality = cms.string( "confirmed" )
    )
    process.hltMuonTkRelIsolationCut0p07Map = cms.EDProducer( "L3MuonCombinedRelativeIsolationProducer",
        printDebug = cms.bool( False ),
        CutsPSet = cms.PSet( 
          applyCutsORmaxNTracks = cms.bool( False ),
          maxNTracks = cms.int32( -1 ),
          Thresholds = cms.vdouble( 0.07 ),
          EtaBounds = cms.vdouble( 2.411 ),
          ComponentName = cms.string( "SimpleCuts" ),
          ConeSizes = cms.vdouble( 0.3 )
        ),
        OutputMuIsoDeposits = cms.bool( True ),
        TrackPt_Min = cms.double( -1.0 ),
        CaloDepositsLabel = cms.InputTag( "notUsed" ),
        CaloExtractorPSet = cms.PSet( 
          DR_Veto_H = cms.double( 0.1 ),
          Vertex_Constraint_Z = cms.bool( False ),
          DR_Veto_E = cms.double( 0.07 ),
          Weight_H = cms.double( 1.0 ),
          CaloTowerCollectionLabel = cms.InputTag( "hltTowerMakerForAll" ),
          DR_Max = cms.double( 0.3 ),
          DepositLabel = cms.untracked.string( "EcalPlusHcal" ),
          Vertex_Constraint_XY = cms.bool( False ),
          Threshold_H = cms.double( 0.5 ),
          Threshold_E = cms.double( 0.2 ),
          ComponentName = cms.string( "CaloExtractor" ),
          Weight_E = cms.double( 1.0 )
        ),
        inputMuonCollection = cms.InputTag( "hltIterL3MuonCandidates" ),
        TrkExtractorPSet = cms.PSet( 
          Diff_z = cms.double( 0.2 ),
          inputTrackCollection = cms.InputTag( "hltIter2L3MuonMerged" ),
          Chi2Ndof_Max = cms.double( 1.0E64 ),
          BeamSpotLabel = cms.InputTag( "hltOnlineBeamSpot" ),
          DR_Veto = cms.double( 0.01 ),
          Pt_Min = cms.double( -1.0 ),
          VetoLeadingTrack = cms.bool( True ),
          DR_Max = cms.double( 0.3 ),
          DepositLabel = cms.untracked.string( "PXLS" ),
          PtVeto_Min = cms.double( 2.0 ),
          NHits_Min = cms.uint32( 0 ),
          PropagateTracksToRadius = cms.bool( True ),
          ReferenceRadius = cms.double( 6.0 ),
          Chi2Prob_Min = cms.double( -1.0 ),
          Diff_r = cms.double( 0.1 ),
          BeamlineOption = cms.string( "BeamSpotFromEvent" ),
          ComponentName = cms.string( "PixelTrackExtractor" ),
          DR_VetoPt = cms.double( 0.025 )
        ),
        UseRhoCorrectedCaloDeposits = cms.bool( False ),
        UseCaloIso = cms.bool( False )
    )

    process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07 = cms.EDFilter( "HLTMuonIsoFilter",
        saveTags = cms.bool( True ),
        PreviousCandTag = cms.InputTag( "hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q" ),  ##trk only
        ##PreviousCandTag = cms.InputTag( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFilteredEB0p14EE0p10"), #ecal + trk
        ##PreviousCandTag = cms.InputTag( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFilteredHB0p16HE0p20" ), ##ecal+hcal+trk
        ##PreviousCandTag = cms.InputTag( "hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhgcalIsoRhoFilteredHGB0p14HGE0p10" ), # this accounts for the HCal+Ecal+HGCal and Trk based isolation
        MinN = cms.int32( 1 ),
        IsolatorPSet = cms.PSet(  ),
        CandTag = cms.InputTag( "hltIterL3MuonCandidates" ),
        DepTag = cms.VInputTag( 'hltMuonTkRelIsolationCut0p07Map' )
    )


    process.HLTIterativeTrackingL3MuonIter02 = cms.Sequence(process.HLTIterativeTrackingL3MuonIteration0 +
                                                            process.HLTIterativeTrackingL3MuonIteration2 +
                                                            process.hltIter2L3MuonMerged )


    process.HLTTrackReconstructionForIsoL3MuonIter02 = cms.Sequence( 
      process.HLTPixelTrackingL3Muon +
      process.HLTIterativeTrackingL3MuonIter02 )


    process.HLTMu24IsolationSequence = cms.Sequence( 
      process.HLTL3muonEcalPFisorecoSequenceNoBoolsForMuons + 
      cms.ignore(process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfecalIsoRhoFilteredEB0p14EE0p10) + 
      process.HLTL3muonHcalPFisorecoSequenceNoBoolsForMuons + 
      cms.ignore(process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhcalIsoRhoFilteredHB0p16HE0p20) + 
      process.HLTL3muonHgcalPFisorecoSequenceNoBoolsForMuons +
      cms.ignore(process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3pfhgcalIsoRhoFilteredHGB0p14HGE0p10) +
      process.HLTTrackReconstructionForIsoL3MuonIter02 + 
      process.hltMuonTkRelIsolationCut0p07Map )

    process.hltTriggerSummaryAOD = cms.EDProducer( "TriggerSummaryProducerAOD",
        moduleLabelPatternsToSkip = cms.vstring(  ),
        processName = cms.string( "@" ),
        throw = cms.bool( False ),
        moduleLabelPatternsToMatch = cms.vstring( 'hlt*' )
    )


    # process.HLT_IsoMu24_v11 = cms.Path(
    #   process.HLTBeginSequence + 
    #   cms.ignore(process.hltL1sSingleMu22) + 
      
    #   process.hltPreIsoMu24 + 
    #   cms.ignore(process.hltL1fL1sMu22L1Filtered0) + 
                                       
    #   process.HLTL2muonrecoSequence + 
    #   cms.ignore(process.hltL2fL1sSingleMu22L1f0L2Filtered10Q) + 
      
    #   process.HLTL3muonrecoSequence + 
    #   cms.ignore(process.hltL1fForIterL3L1fL1sMu22L1Filtered0) + 
    #   cms.ignore(process.hltL3fL1sSingleMu22L1f0L2f10QL3Filtered24Q) +
                                       
    #   process.bunchSpacingProducer+
    #   process.HLTMu24IsolationSequence + 
    #   cms.ignore(process.hltL3crIsoL1sSingleMu22L1f0L2f10QL3f24QL3trkIsoFiltered0p07) +
       
    #   process.hltTriggerSummaryAOD +
    #   process.HLTEndSequence )


                      
    ##### ESProducers with naming used in the Muon HLT modules
    ## corresponding to process.BeamHaloSHPropagatorAny 
    process.hltESPFastSteppingHelixPropagatorAny = cms.ESProducer("SteppingHelixPropagatorESProducer",
        ApplyRadX0Correction = cms.bool(True),
        AssumeNoMaterial = cms.bool(False),
        ComponentName = cms.string('hltESPFastSteppingHelixPropagatorAny'),
        NoErrorPropagation = cms.bool(False),
        PropagationDirection = cms.string('anyDirection'),
        SetVBFPointer = cms.bool(False),
        VBFName = cms.string('VolumeBasedMagneticField'),
        debug = cms.bool(False),
        endcapShiftInZNeg = cms.double(0.0),
        endcapShiftInZPos = cms.double(0.0),
        returnTangentPlane = cms.bool(True),
        sendLogWarning = cms.bool(False),
        useEndcapShiftsInZ = cms.bool(False),
        useInTeslaFromMagField = cms.bool(False),
        useIsYokeFlag = cms.bool(True),
        useMagVolumes = cms.bool(True),
        useMatVolumes = cms.bool(True),
        useTuningForL2Speed = cms.bool(True)
    )

    ## corresponding to process.BeamHaloSHPropagatorOpposite
    process.hltESPFastSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
        ApplyRadX0Correction = cms.bool(True),
        AssumeNoMaterial = cms.bool(False),
        ComponentName = cms.string('hltESPFastSteppingHelixPropagatorOpposite'),
        NoErrorPropagation = cms.bool(False),
        PropagationDirection = cms.string('oppositeToMomentum'),
        SetVBFPointer = cms.bool(False),
        VBFName = cms.string('VolumeBasedMagneticField'),
        debug = cms.bool(False),
        endcapShiftInZNeg = cms.double(0.0),
        endcapShiftInZPos = cms.double(0.0),
        returnTangentPlane = cms.bool(True),
        sendLogWarning = cms.bool(False),
        useEndcapShiftsInZ = cms.bool(False),
        useInTeslaFromMagField = cms.bool(False),
        useIsYokeFlag = cms.bool(True),
        useMagVolumes = cms.bool(True),
        useMatVolumes = cms.bool(True),
        useTuningForL2Speed = cms.bool(True)
    )

    process.hltESPMuonTransientTrackingRecHitBuilder = cms.ESProducer("MuonTransientTrackingRecHitBuilderESProducer",
        ComponentName = cms.string('hltESPMuonTransientTrackingRecHitBuilder')
    )


    process.hltESPKFUpdator = cms.ESProducer("KFUpdatorESProducer",
        ComponentName = cms.string('hltESPKFUpdator')
    )
    process.hltESPDummyDetLayerGeometry = cms.ESProducer("DetLayerGeometryESProducer",
        ComponentName = cms.string('hltESPDummyDetLayerGeometry')
    )
    process.hltESPChi2MeasurementEstimator30 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
        ComponentName = cms.string('hltESPChi2MeasurementEstimator30'),
        MaxChi2 = cms.double(30.0),
        MaxDisplacement = cms.double(100.0),
        MaxSagitta = cms.double(-1.0),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
        MinimalTolerance = cms.double(10.0),
        appendToDataLabel = cms.string(''),
        nSigma = cms.double(3.0)
    )

    process.hltESPKFTrajectorySmootherForMuonTrackLoader = cms.ESProducer("KFTrajectorySmootherESProducer",
        ComponentName = cms.string('hltESPKFTrajectorySmootherForMuonTrackLoader'),
        Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
        Propagator = cms.string('hltESPSmartPropagatorAnyOpposite'),
        RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
        Updator = cms.string('hltESPKFUpdator'),
        appendToDataLabel = cms.string(''),
        errorRescaling = cms.double(10.0),
        minHits = cms.int32(3)
    )


    #it's the same of the BeamHaloSHPropagatorOpposite 
    process.hltESPSteppingHelixPropagatorOpposite = cms.ESProducer("SteppingHelixPropagatorESProducer",
        ApplyRadX0Correction = cms.bool(True),
        AssumeNoMaterial = cms.bool(False),
        ComponentName = cms.string('hltESPSteppingHelixPropagatorOpposite'),
        NoErrorPropagation = cms.bool(False),
        PropagationDirection = cms.string('oppositeToMomentum'),
        SetVBFPointer = cms.bool(False),
        VBFName = cms.string('VolumeBasedMagneticField'),
        debug = cms.bool(False),
        endcapShiftInZNeg = cms.double(0.0),
        endcapShiftInZPos = cms.double(0.0),
        returnTangentPlane = cms.bool(True),
        sendLogWarning = cms.bool(False),
        useEndcapShiftsInZ = cms.bool(False),
        useInTeslaFromMagField = cms.bool(False),
        useIsYokeFlag = cms.bool(True),
        useMagVolumes = cms.bool(True),
        useMatVolumes = cms.bool(True),
        useTuningForL2Speed = cms.bool(False)
    )

    process.hltESPChi2MeasurementEstimator100 = cms.ESProducer("Chi2MeasurementEstimatorESProducer",
        ComponentName = cms.string('hltESPChi2MeasurementEstimator100'),
        MaxChi2 = cms.double(40.0),
        MaxDisplacement = cms.double(0.5),
        MaxSagitta = cms.double(2.0),
        MinPtForHitRecoveryInGluedDet = cms.double(1e+12),
        MinimalTolerance = cms.double(0.5),
        appendToDataLabel = cms.string(''),
        nSigma = cms.double(4.0)
    )

    ##specific for muons, similar to the process.initialStepChi2Est 
    process.hltESPChi2ChargeMeasurementEstimator30 = cms.ESProducer("Chi2ChargeMeasurementEstimatorESProducer",
        ComponentName = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        MaxChi2 = cms.double(30.0),
        MaxDisplacement = cms.double(100.0),
        MaxSagitta = cms.double(-1.0),
        MinPtForHitRecoveryInGluedDet = cms.double(1000000.0),
        MinimalTolerance = cms.double(10.0),
        appendToDataLabel = cms.string(''),
        clusterChargeCut = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        nSigma = cms.double(3.0),
        pTChargeCutThreshold = cms.double(-1.0)
    )

    ##re-defined to get the naming used for muon HLT
    process.hltESPMeasurementTracker = cms.ESProducer("MeasurementTrackerESProducer",
        ComponentName = cms.string('hltESPMeasurementTracker'),
        DebugPixelModuleQualityDB = cms.untracked.bool(False),
        DebugPixelROCQualityDB = cms.untracked.bool(False),
        DebugStripAPVFiberQualityDB = cms.untracked.bool(False),
        DebugStripModuleQualityDB = cms.untracked.bool(False),
        DebugStripStripQualityDB = cms.untracked.bool(False),
        HitMatcher = cms.string('StandardMatcher'),
        MaskBadAPVFibers = cms.bool(True),
        #PixelCPE = cms.string('hltESPPixelCPEGeneric'),
        PixelCPE = cms.string('PixelCPEGeneric'),
        SiStripQualityLabel = cms.string(''),
        StripCPE = cms.string('hltESPStripCPEfromTrackAngle'),
        UsePixelModuleQualityDB = cms.bool(True),
        UsePixelROCQualityDB = cms.bool(True),
        UseStripAPVFiberQualityDB = cms.bool(True),
        UseStripModuleQualityDB = cms.bool(True),
        UseStripStripQualityDB = cms.bool(True),
        badStripCuts = cms.PSet(
            TEC = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TIB = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TID = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            ),
            TOB = cms.PSet(
                maxBad = cms.uint32(4),
                maxConsecutiveBad = cms.uint32(2)
            )
        )
    )

    process.hltESPRKTrajectorySmoother = cms.ESProducer("KFTrajectorySmootherESProducer",
        ComponentName = cms.string('hltESPRKTrajectorySmoother'),
        Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
        Updator = cms.string('hltESPKFUpdator'),
        appendToDataLabel = cms.string(''),
        errorRescaling = cms.double(100.0),
        minHits = cms.int32(3)
    )

    process.hltESPGlobalDetLayerGeometry = cms.ESProducer("GlobalDetLayerGeometryESProducer",
        ComponentName = cms.string('hltESPGlobalDetLayerGeometry')
    )

    process.hltESPRKTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
        ComponentName = cms.string('hltESPRKTrajectoryFitter'),
        Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
        Propagator = cms.string('hltESPRungeKuttaTrackerPropagator'),
        RecoGeometry = cms.string('hltESPGlobalDetLayerGeometry'),
        Updator = cms.string('hltESPKFUpdator'),
        appendToDataLabel = cms.string(''),
        minHits = cms.int32(3)
    )

    process.hltESPRungeKuttaTrackerPropagator = cms.ESProducer("PropagatorWithMaterialESProducer",
        ComponentName = cms.string('hltESPRungeKuttaTrackerPropagator'),
        Mass = cms.double(0.105),
        MaxDPhi = cms.double(1.6),
        PropagationDirection = cms.string('alongMomentum'),
        SimpleMagneticField = cms.string(''),
        ptMin = cms.double(-1.0),
        useRungeKutta = cms.bool(True)
    )

    process.hltESPKFFittingSmootherWithOutliersRejectionAndRK = cms.ESProducer("KFFittingSmootherESProducer",
        BreakTrajWith2ConsecutiveMissing = cms.bool(True),
        ComponentName = cms.string('hltESPKFFittingSmootherWithOutliersRejectionAndRK'),
        EstimateCut = cms.double(20.0),
        Fitter = cms.string('hltESPRKTrajectoryFitter'),
        LogPixelProbabilityCut = cms.double(-14.0),
        MaxFractionOutliers = cms.double(0.3),
        MaxNumberOfOutliers = cms.int32(3),
        MinDof = cms.int32(2),
        MinNumberOfHits = cms.int32(3),
        NoInvalidHitsBeginEnd = cms.bool(True),
        NoOutliersBeginEnd = cms.bool(False),
        RejectTracks = cms.bool(True),
        Smoother = cms.string('hltESPRKTrajectorySmoother'),
        appendToDataLabel = cms.string('')
    )

    process.hltESPSmartPropagatorAnyOpposite = cms.ESProducer("SmartPropagatorESProducer",
        ComponentName = cms.string('hltESPSmartPropagatorAnyOpposite'),
        Epsilon = cms.double(5.0),
        MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
        PropagationDirection = cms.string('oppositeToMomentum'),
        TrackerPropagator = cms.string('PropagatorWithMaterialOpposite')
    )

    process.hltESPSmartPropagatorAny = cms.ESProducer("SmartPropagatorESProducer",
        ComponentName = cms.string('hltESPSmartPropagatorAny'),
        Epsilon = cms.double(5.0),
        MuonPropagator = cms.string('SteppingHelixPropagatorAny'),
        PropagationDirection = cms.string('alongMomentum'),
        TrackerPropagator = cms.string('PropagatorWithMaterial')
    )

    process.hltESPSmartPropagator = cms.ESProducer("SmartPropagatorESProducer",
        ComponentName = cms.string('hltESPSmartPropagator'),
        Epsilon = cms.double(5.0),
        MuonPropagator = cms.string('hltESPSteppingHelixPropagatorAlong'),
        PropagationDirection = cms.string('alongMomentum'),
        TrackerPropagator = cms.string('PropagatorWithMaterial')
    )

    process.hltESPL3MuKFTrajectoryFitter = cms.ESProducer("KFTrajectoryFitterESProducer",
        ComponentName = cms.string('hltESPL3MuKFTrajectoryFitter'),
        Estimator = cms.string('hltESPChi2MeasurementEstimator30'),
        Propagator = cms.string('hltESPSmartPropagatorAny'),
        RecoGeometry = cms.string('hltESPDummyDetLayerGeometry'),
        Updator = cms.string('hltESPKFUpdator'),
        appendToDataLabel = cms.string(''),
        minHits = cms.int32(3)
    )

    process.hltESPSteppingHelixPropagatorAlong = cms.ESProducer("SteppingHelixPropagatorESProducer",
        ApplyRadX0Correction = cms.bool(True),
        AssumeNoMaterial = cms.bool(False),
        ComponentName = cms.string('hltESPSteppingHelixPropagatorAlong'),
        NoErrorPropagation = cms.bool(False),
        PropagationDirection = cms.string('alongMomentum'),
        SetVBFPointer = cms.bool(False),
        VBFName = cms.string('VolumeBasedMagneticField'),
        debug = cms.bool(False),
        endcapShiftInZNeg = cms.double(0.0),
        endcapShiftInZPos = cms.double(0.0),
        returnTangentPlane = cms.bool(True),
        sendLogWarning = cms.bool(False),
        useEndcapShiftsInZ = cms.bool(False),
        useInTeslaFromMagField = cms.bool(False),
        useIsYokeFlag = cms.bool(True),
        useMagVolumes = cms.bool(True),
        useMatVolumes = cms.bool(True),
        useTuningForL2Speed = cms.bool(False)
    )

    #process.hltESPTTRHBuilderPixelOnly = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
    #    ComponentName = cms.string('hltESPTTRHBuilderPixelOnly'),
    #    ComputeCoarseLocalPositionFromDisk = cms.bool(False),
    #    Matcher = cms.string('StandardMatcher'),
    #    #Phase2StripCPE = cms.string('Phase2StripCPE'),
    #    Phase2StripCPE = cms.string(''),
    #    PixelCPE = cms.string('PixelCPEGeneric'),
    #    StripCPE = cms.string('Fake')
    #)

    ###### to be used instead of hltESPTTRHBuilderPixelOnly ??
    process.ttrhbwr = cms.ESProducer("TkTransientTrackingRecHitBuilderESProducer",
        ComponentName = cms.string('WithTrackAngle'),
        ComputeCoarseLocalPositionFromDisk = cms.bool(False),
        Matcher = cms.string('StandardMatcher'),
        Phase2StripCPE = cms.string('Phase2StripCPE'),
        PixelCPE = cms.string('PixelCPEGeneric'),
        StripCPE = cms.string('StripCPEfromTrackAngle')
    )


    ### exists already,but re-named to get the same naming of muon HLT
    process.hltPixelTracksCleanerBySharedHits = cms.ESProducer("PixelTrackCleanerBySharedHitsESProducer",
        ComponentName = cms.string('hltPixelTracksCleanerBySharedHits'),
        appendToDataLabel = cms.string(''),
        useQuadrupletAlgo = cms.bool(False)
    )

    process.hltESPTrackAlgoPriorityOrder = cms.ESProducer("TrackAlgoPriorityOrderESProducer",
        ComponentName = cms.string('hltESPTrackAlgoPriorityOrder'),
        algoOrder = cms.vstring(),
        appendToDataLabel = cms.string('')
    )

    process.hltESPTrajectoryCleanerBySharedHits = cms.ESProducer("TrajectoryCleanerESProducer",
        ComponentName = cms.string('hltESPTrajectoryCleanerBySharedHits'),
        ComponentType = cms.string('TrajectoryCleanerBySharedHits'),
        MissingHitPenalty = cms.double(0.0),
        ValidHitBonus = cms.double(100.0),
        allowSharedFirstHit = cms.bool(False),
        fractionShared = cms.double(0.5)
    )

    ###PSet
    #process.HLTPSetPvClusterComparerForIT = cms.PSet(
    #    track_chi2_max = cms.double(20.0),
    #    track_prob_min = cms.double(-1.0),
    #    track_pt_max = cms.double(20.0),
    #    track_pt_min = cms.double(1.0)
    #)

    ### use this instead of HLTPSetPVClusterComparerForIT 
    process.hltPhase2PSetPvClusterComparerForIT = cms.PSet(
      track_chi2_max = cms.double( 20.0 ),
      track_pt_max = cms.double( 20.0 ),
      track_prob_min = cms.double( -1.0 ),
      track_pt_min = cms.double( 1.0 )
    )

    process.HLTSiStripClusterChargeCutNone = cms.PSet(
        value = cms.double(-1.0)
    )

    process.HLTPSetMuonCkfTrajectoryFilter = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(1),
        maxLostHitsFraction = cms.double(999.0),
        maxNumberOfHits = cms.int32(-1),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(5),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.HLTPSetMuonCkfTrajectoryBuilder = cms.PSet(
        ComponentType = cms.string('MuonCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string('hltESPMeasurementTracker'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(True),
        deltaEta = cms.double(-1.0),
        deltaPhi = cms.double(-1.0),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        intermediateCleaning = cms.bool(False),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(5),
        propagatorAlong = cms.string('PropagatorWithMaterial'),
        propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
        propagatorProximity = cms.string('SteppingHelixPropagatorAny'),
        rescaleErrorIfFail = cms.double(1.0),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTPSetMuonCkfTrajectoryFilter')
        ),
        updator = cms.string('hltESPKFUpdator'),
        useSeedLayer = cms.bool(False),
        seedAs5DHit = cms.bool(False),
    )

    process.HLTIter2IterL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string('hltIter2HighPtTkMuESPMeasurementTracker'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        foundHitBonus = cms.double(1000.0),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(False),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(2),
        minNrOfHitsForRebuild = cms.int32(5),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        requireSeedHitsInRebuild = cms.bool(False),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter2IterL3MuonPSetTrajectoryFilterIT')
        ),
        updator = cms.string('hltESPKFUpdator'),
        useSameTrajFilter = cms.bool(True),
        seedAs5DHit = cms.bool(False),
    )

    process.HLTIter2IterL3MuonPSetTrajectoryFilterIT = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(3),
        maxLostHits = cms.int32(1),
        maxLostHitsFraction = cms.double(999.0),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.3),
        minimumNumberOfHits = cms.int32(5),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(10.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(999),
        maxLostHitsFraction = cms.double(0.1),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(3),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.HLTIter0IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(True),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        foundHitBonus = cms.double(1000.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT')
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(True),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(1.0),
        maxCand = cms.int32(5),
        minNrOfHitsForRebuild = cms.int32(2),
        propagatorAlong = cms.string('PropagatorWithMaterial'),
        propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
        requireSeedHitsInRebuild = cms.bool(True),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3FromL1MuonGroupedCkfTrajectoryFilterIT')
        ),
        updator = cms.string('hltESPKFUpdator'),
        useSameTrajFilter = cms.bool(True),
        seedAs5DHit = cms.bool(False),
    )

    process.HLTIter2IterL3FromL1MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string('hltIter2HighPtTkMuESPMeasurementTracker'),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(False),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        foundHitBonus = cms.double(1000.0),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(False),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(30.0),
        maxCand = cms.int32(2),
        minNrOfHitsForRebuild = cms.int32(5),
        propagatorAlong = cms.string('PropagatorWithMaterialParabolicMf'),
        propagatorOpposite = cms.string('PropagatorWithMaterialParabolicMfOpposite'),
        requireSeedHitsInRebuild = cms.bool(False),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter2IterL3FromL1MuonPSetTrajectoryFilterIT')
        ),
        updator = cms.string('hltESPKFUpdator'),
        useSameTrajFilter = cms.bool(True),
        seedAs5DHit = cms.bool(False),
    )

    process.HLTIter2IterL3FromL1MuonPSetTrajectoryFilterIT = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(1.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(3),
        maxLostHits = cms.int32(1),
        maxLostHitsFraction = cms.double(999.0),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.3),
        minimumNumberOfHits = cms.int32(5),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )


    #process.HLTSeedFromProtoTracks = cms.PSet(
    #    ComponentName = cms.string('SeedFromConsecutiveHitsCreator'),
    #    MinOneOverPtError = cms.double(1.0),
    #    OriginTransverseErrorMultiplier = cms.double(1.0),
    #    SeedMomentumForBOFF = cms.double(5.0),
    #    TTRHBuilder = cms.string('hltESPTTRHBuilderPixelOnly'),
    #    forceKinematicWithRegionDirection = cms.bool(False),
    #    magneticField = cms.string('ParabolicMf'),
    #    propagator = cms.string('PropagatorWithMaterialParabolicMf')
    #)

    #### use this one instead of process.HLTSeedFromProtoTracks
    process.hltPhase2SeedFromProtoTracks = cms.PSet(
      ComponentName = cms.string("SeedFromConsecutiveHitsCreator" ),
      MinOneOverPtError = cms.double( 1.0 ),
      OriginTransverseErrorMultiplier = cms.double( 1.0 ),
      SeedMomentumForBOFF = cms.double( 5.0 ),
      TTRHBuilder = cms.string("WithTrackAngle"), 
      forceKinematicWithRegionDirection = cms.bool( False ),
      magneticField = cms.string(""),	 
      propagator = cms.string("PropagatorWithMaterial")	  
    )



    process.HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT = cms.PSet(
        ComponentType = cms.string('CkfBaseTrajectoryFilter'),
        chargeSignificance = cms.double(-1.0),
        constantValueForLostHitsFractionFilter = cms.double(10.0),
        extraNumberOfHitsBeforeTheFirstLoop = cms.int32(4),
        maxCCCLostHits = cms.int32(9999),
        maxConsecLostHits = cms.int32(1),
        maxLostHits = cms.int32(999),
        maxLostHitsFraction = cms.double(0.1),
        maxNumberOfHits = cms.int32(100),
        minGoodStripCharge = cms.PSet(
            refToPSet_ = cms.string('HLTSiStripClusterChargeCutNone')
        ),
        minHitsMinPt = cms.int32(3),
        minNumberOfHitsForLoopers = cms.int32(13),
        minNumberOfHitsPerLoop = cms.int32(4),
        minPt = cms.double(0.9),
        minimumNumberOfHits = cms.int32(3),
        nSigmaMinPt = cms.double(5.0),
        pixelSeedExtension = cms.bool(False),
        seedExtension = cms.int32(0),
        seedPairPenalty = cms.int32(0),
        strictSeedExtension = cms.bool(False)
    )

    process.HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string(''),
        TTRHBuilder = cms.string('WithTrackAngle'),
        alwaysUseInvalidHits = cms.bool(True),
        bestHitOnly = cms.bool(True),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        foundHitBonus = cms.double(1000.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
        ),
        intermediateCleaning = cms.bool(True),
        keepOriginalIfRebuildFails = cms.bool(True),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(1.0),
        maxCand = cms.int32(5),
        minNrOfHitsForRebuild = cms.int32(2),
        propagatorAlong = cms.string('PropagatorWithMaterial'),
        propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
        requireSeedHitsInRebuild = cms.bool(True),
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
        ),
        updator = cms.string('hltESPKFUpdator'),
        useSameTrajFilter = cms.bool(True),
        seedAs5DHit = cms.bool(False),
    )


    process.HLTIter0IterL3MuonPSetGroupedCkfTrajectoryBuilderIT = cms.PSet(
        useSameTrajFilter = cms.bool(True),    
        ComponentType = cms.string('GroupedCkfTrajectoryBuilder'),
        MeasurementTrackerName = cms.string(''),
        keepOriginalIfRebuildFails = cms.bool(True),
        lockHits = cms.bool(True),
        lostHitPenalty = cms.double(1.0),
        requireSeedHitsInRebuild = cms.bool(True),
        TTRHBuilder = cms.string('WithTrackAngle'),
        propagatorOpposite = cms.string('PropagatorWithMaterialOpposite'),
        
        trajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
        ),
        propagatorAlong = cms.string('PropagatorWithMaterial'),
        minNrOfHitsForRebuild = cms.int32(2),
        maxCand = cms.int32(5),
        alwaysUseInvalidHits = cms.bool(True),
        estimator = cms.string('hltESPChi2ChargeMeasurementEstimator30'),
        foundHitBonus = cms.double(1000.0),
        inOutTrajectoryFilter = cms.PSet(
            refToPSet_ = cms.string('HLTIter0IterL3MuonGroupedCkfTrajectoryFilterIT')
        ),
        intermediateCleaning = cms.bool(True),
        updator = cms.string('hltESPKFUpdator'),
        bestHitOnly = cms.bool(True),
        seedAs5DHit = cms.bool(False)
    )

    process.HLTIter0GroupedCkfTrajectoryBuilderIT = cms.PSet( 
      keepOriginalIfRebuildFails = cms.bool( False ),
      lockHits = cms.bool( True ),
      maxDPhiForLooperReconstruction = cms.double( 2.0 ),
      propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
      trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter0PSetTrajectoryFilterIT" ) ),
      doSeedingRegionRebuilding = cms.bool( False ),
      useHitsSplitting = cms.bool( False ),
      maxCand = cms.int32( 2 ),
      estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator9" ),
      intermediateCleaning = cms.bool( True ),
      bestHitOnly = cms.bool( True ),
      useSameTrajFilter = cms.bool( True ),
      MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
      ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
      lostHitPenalty = cms.double( 30.0 ),
      requireSeedHitsInRebuild = cms.bool( True ),
      TTRHBuilder = cms.string( "WithTrackAngle" ),
      maxPtForLooperReconstruction = cms.double( 0.7 ),
      cleanTrajectoryAfterInOut = cms.bool( False ),
      propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
      minNrOfHitsForRebuild = cms.int32( 5 ),
      alwaysUseInvalidHits = cms.bool( False ),
      inOutTrajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter0PSetTrajectoryFilterIT" ) ),
      foundHitBonus = cms.double( 5.0 ),
      updator = cms.string( "hltESPKFUpdator" ),
      seedAs5DHit = cms.bool(False)
    )

    process.HLTIter0PSetTrajectoryFilterIT = cms.PSet( 
      minimumNumberOfHits = cms.int32( 4 ),
      ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
      seedExtension = cms.int32( 0 ),
      chargeSignificance = cms.double( -1.0 ),
      pixelSeedExtension = cms.bool( False ),
      strictSeedExtension = cms.bool( False ),
      nSigmaMinPt = cms.double( 5.0 ),
      maxCCCLostHits = cms.int32( 0 ),
      minPt = cms.double( 0.3 ),
      maxConsecLostHits = cms.int32( 1 ),
      extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
      constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
      seedPairPenalty = cms.int32( 0 ),
      maxNumberOfHits = cms.int32( 100 ),
      minNumberOfHitsForLoopers = cms.int32( 13 ),
      minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
      minNumberOfHitsPerLoop = cms.int32( 4 ),
      minHitsMinPt = cms.int32( 4 ),
      maxLostHitsFraction = cms.double( 999.0 ),
      maxLostHits = cms.int32( 1 )
    )

    process.HLTSiStripClusterChargeCutLoose = cms.PSet(  value = cms.double( 1620.0 ) )
    process.hltESPChi2ChargeMeasurementEstimator9 = cms.ESProducer( "Chi2ChargeMeasurementEstimatorESProducer",
      appendToDataLabel = cms.string( "" ),
      clusterChargeCut = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutLoose" ) ),
      MinimalTolerance = cms.double( 0.5 ),
      MaxDisplacement = cms.double( 0.5 ),
      ComponentName = cms.string( "hltESPChi2ChargeMeasurementEstimator9" ),
      pTChargeCutThreshold = cms.double( 15.0 ),
      nSigma = cms.double( 3.0 ),
      MaxSagitta = cms.double( 2.0 ),
      MaxChi2 = cms.double( 9.0 ),
      MinPtForHitRecoveryInGluedDet = cms.double( 1000000.0 )
    )


    process.HLTIter1GroupedCkfTrajectoryBuilderIT = cms.PSet( 
      useSameTrajFilter = cms.bool( True ),
      ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
      MeasurementTrackerName = cms.string( "hltIter1ESPMeasurementTracker" ),
      keepOriginalIfRebuildFails = cms.bool( False ),
      lostHitPenalty = cms.double( 30.0 ),
      lockHits = cms.bool( True ),
      requireSeedHitsInRebuild = cms.bool( True ),
      TTRHBuilder = cms.string( "WithTrackAngle" ),
      propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
      trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter1PSetTrajectoryFilterIT" ) ),
      propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
      minNrOfHitsForRebuild = cms.int32( 5 ),
      maxCand = cms.int32( 2 ),
      alwaysUseInvalidHits = cms.bool( False ),
      estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
      intermediateCleaning = cms.bool( True ),
      foundHitBonus = cms.double( 5.0 ),
      updator = cms.string( "hltESPKFUpdator" ),
      bestHitOnly = cms.bool( True ),
      seedAs5DHit = cms.bool(False)
    )

    process.HLTIter1PSetTrajectoryFilterIT = cms.PSet( 
      minimumNumberOfHits = cms.int32( 3 ),
      ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
      seedExtension = cms.int32( 0 ),
      chargeSignificance = cms.double( -1.0 ),
      pixelSeedExtension = cms.bool( False ),
      strictSeedExtension = cms.bool( False ),
      nSigmaMinPt = cms.double( 5.0 ),
      maxCCCLostHits = cms.int32( 0 ),
      minPt = cms.double( 0.2 ),
      maxConsecLostHits = cms.int32( 1 ),
      extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
      constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
      seedPairPenalty = cms.int32( 0 ),
      maxNumberOfHits = cms.int32( 100 ),
      minNumberOfHitsForLoopers = cms.int32( 13 ),
      minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
      minNumberOfHitsPerLoop = cms.int32( 4 ),
      minHitsMinPt = cms.int32( 3 ),
      maxLostHitsFraction = cms.double( 999.0 ),
      maxLostHits = cms.int32( 1 )
    )

    process.hltESPChi2ChargeMeasurementEstimator16 = cms.ESProducer( "Chi2ChargeMeasurementEstimatorESProducer",
      appendToDataLabel = cms.string( "" ),
      clusterChargeCut = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutLoose" ) ),
      MinimalTolerance = cms.double( 0.5 ),
      MaxDisplacement = cms.double( 0.5 ),
      ComponentName = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
      pTChargeCutThreshold = cms.double( -1.0 ),
      nSigma = cms.double( 3.0 ),
      MaxSagitta = cms.double( 2.0 ),
      MaxChi2 = cms.double( 16.0 ),
      MinPtForHitRecoveryInGluedDet = cms.double( 1000000.0 )
    )

    process.HLTIter2GroupedCkfTrajectoryBuilderIT = cms.PSet( 
      keepOriginalIfRebuildFails = cms.bool( False ),
      lockHits = cms.bool( True ),
      maxDPhiForLooperReconstruction = cms.double( 2.0 ),
      propagatorOpposite = cms.string( "PropagatorWithMaterialParabolicMfOpposite" ),
      trajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter2PSetTrajectoryFilterIT" ) ),
      doSeedingRegionRebuilding = cms.bool( False ),
      useHitsSplitting = cms.bool( False ),
      maxCand = cms.int32( 2 ),
      estimator = cms.string( "hltESPChi2ChargeMeasurementEstimator16" ),
      intermediateCleaning = cms.bool( True ),
      bestHitOnly = cms.bool( True ),
      useSameTrajFilter = cms.bool( True ),
      MeasurementTrackerName = cms.string( "hltESPMeasurementTracker" ),
      ComponentType = cms.string( "GroupedCkfTrajectoryBuilder" ),
      lostHitPenalty = cms.double( 30.0 ),
      requireSeedHitsInRebuild = cms.bool( True ),
      TTRHBuilder = cms.string( "WithTrackAngle" ),
      maxPtForLooperReconstruction = cms.double( 0.7 ),
      cleanTrajectoryAfterInOut = cms.bool( False ),
      propagatorAlong = cms.string( "PropagatorWithMaterialParabolicMf" ),
      minNrOfHitsForRebuild = cms.int32( 5 ),
      alwaysUseInvalidHits = cms.bool( False ),
      inOutTrajectoryFilter = cms.PSet(  refToPSet_ = cms.string( "HLTIter2PSetTrajectoryFilterIT" ) ),
      foundHitBonus = cms.double( 5.0 ),
      updator = cms.string( "hltESPKFUpdator" ),
      seedAs5DHit = cms.bool(False)
    )

    process.HLTIter2PSetTrajectoryFilterIT = cms.PSet( 
      minimumNumberOfHits = cms.int32( 3 ),
      ComponentType = cms.string( "CkfBaseTrajectoryFilter" ),
      seedExtension = cms.int32( 1 ),
      chargeSignificance = cms.double( -1.0 ),
      pixelSeedExtension = cms.bool( False ),
      strictSeedExtension = cms.bool( False ),
      nSigmaMinPt = cms.double( 5.0 ),
      maxCCCLostHits = cms.int32( 0 ),
      minPt = cms.double( 0.3 ),
      maxConsecLostHits = cms.int32( 1 ),
      extraNumberOfHitsBeforeTheFirstLoop = cms.int32( 4 ),
      constantValueForLostHitsFractionFilter = cms.double( 1.0 ),
      seedPairPenalty = cms.int32( 0 ),
      maxNumberOfHits = cms.int32( 100 ),
      minNumberOfHitsForLoopers = cms.int32( 13 ),
      minGoodStripCharge = cms.PSet(  refToPSet_ = cms.string( "HLTSiStripClusterChargeCutNone" ) ),
      minNumberOfHitsPerLoop = cms.int32( 4 ),
      minHitsMinPt = cms.int32( 3 ),
      maxLostHitsFraction = cms.double( 999.0 ),
      maxLostHits = cms.int32( 1 )
    )

    return process
