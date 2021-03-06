
import FWCore.ParameterSet.Config as cms
from Configuration.StandardSequences.Eras import eras
process = cms.Process("MYHLT", eras.Phase2C9)

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49Reco_cff')
process.load('Configuration.Geometry.GeometryExtended2026D49_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

process.maxEvents = cms.untracked.PSet(
    input  = cms.untracked.int32(100),
    output = cms.optional.untracked.allowed(cms.int32,cms.PSet)
)

process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(''),
    secondaryFileNames = cms.untracked.vstring()
)

from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase2_realistic_T15', '')

# -- L1 emulation -- #
process.load('Configuration.StandardSequences.L1TrackTrigger_cff')
process.load('Configuration.StandardSequences.SimL1Emulator_cff')
process.load('Configuration.StandardSequences.EndOfProcess_cff')
process.L1TrackTrigger_step = cms.Path(process.L1TrackTrigger)
process.L1simulation_step = cms.Path(process.SimL1Emulator)
process.L1TkMuons.L1TrackInputTag = cms.InputTag("TTTracksFromTrackletEmulation", "Level1TTTracks", "RECO")
# -- #

# -- HLTriggerFinalPath -- #
process.hltTriggerSummaryAOD = cms.EDProducer( "TriggerSummaryProducerAOD",
    moduleLabelPatternsToSkip = cms.vstring(  ),
    processName = cms.string( "@" ),
    moduleLabelPatternsToMatch = cms.vstring( 'hlt*' ),
    throw = cms.bool( False )
)
process.hltTriggerSummaryRAW = cms.EDProducer( "TriggerSummaryProducerRAW",
    processName = cms.string( "@" )
)
process.hltBoolFalse = cms.EDFilter( "HLTBool",
    result = cms.bool( False )
)
process.HLTriggerFinalPath = cms.Path(
    process.hltTriggerSummaryAOD+
    process.hltTriggerSummaryRAW+
    process.hltBoolFalse
)
# -- #

# -- L3 Reconstruction and Isolation -- #
from HLTrigger.PhaseII.Muon.Customizers.customizerForPhase2MuonHLT import customizePhase2MuonHLTReconstruction
process = customizePhase2MuonHLTReconstruction(process)

from HLTrigger.PhaseII.Muon.Customizers.customizerForPhase2MuonHLT import customizePhase2MuonHLTIsolation
process = customizePhase2MuonHLTIsolation(process)

for moduleType in [process.producers_(), process.filters_(), process.analyzers_()]:
    for name, module in moduleType.iteritems():
        if hasattr(module, "mightGet") and module.mightGet:
            module.mightGet = cms.optional.untracked.vstring
# -- #

# -- L1T-HLT interface input db -- #
process.load("CondCore.CondDB.CondDB_cfi")
process.CondDB.connect = "sqlite_file:L1TObjScaling.db"

process.L1TScalingESSource = cms.ESSource(
    "PoolDBESSource",
    process.CondDB,
    DumpStat=cms.untracked.bool(True),
    toGet=cms.VPSet(
        cms.PSet(
            record=cms.string("L1TObjScalingRcd"),
            tag=cms.string("L1TkMuonScaling"),
            label=cms.untracked.string("L1TkMuonScaling"),
        ),
    ),
)
process.es_prefer_l1tscaling = cms.ESPrefer("PoolDBESSource", "L1TScalingESSource")

process.hltL1TkSingleMuFiltered22 = cms.EDFilter("L1TkMuonFilter",
    saveTags = cms.bool( True ),
    MinPt = cms.double( 22.0 ),
    inputTag = cms.InputTag("L1TkMuons", "", "MYHLT")
)

process.l1tTripleMuon3 = cms.EDFilter(
    "L1TkMuonFilter",
    MinPt=cms.double(3.0),
    MinN=cms.int32(3),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag = cms.InputTag("L1TkMuons", "", "MYHLT")
)

process.l1tSingleMuon5 = cms.EDFilter(
    "L1TkMuonFilter",
    MinPt=cms.double(5.0),
    MinN=cms.int32(1),
    MinEta=cms.double(-2.4),
    MaxEta=cms.double(2.4),
    inputTag = cms.InputTag("L1TkMuons", "", "MYHLT")
)

process.hltL3fL1TkTripleMu533PreFiltered555 = cms.EDFilter( "HLTMuonTrkL1TkMuFilter",
    saveTags = cms.bool( True ),
    maxNormalizedChi2 = cms.double( 1.0E99 ),
    maxAbsEta = cms.double( 2.5 ),
    minPt = cms.double( 5.0 ),
    minN = cms.uint32( 3 ),
    minMuonStations = cms.int32( 1 ),
    minMuonHits = cms.int32( -1 ),
    minTrkHits = cms.int32( -1 ),
    previousCandTag = cms.InputTag( "l1tTripleMuon3" ),
    inputMuonCollection = cms.InputTag( "hltPhase2L3Muons" ),
    inputCandCollection = cms.InputTag( "hltPhase2L3MuonCandidates" )
)
process.hltL3fL1TkTripleMu533L3Filtered1055 = cms.EDFilter( "HLTMuonTrkL1TkMuFilter",
    saveTags = cms.bool( True ),
    maxNormalizedChi2 = cms.double( 1.0E99 ),
    maxAbsEta = cms.double( 2.5 ),
    minPt = cms.double( 10.0 ),
    minN = cms.uint32( 1 ),
    minMuonStations = cms.int32( 1 ),
    minMuonHits = cms.int32( -1 ),
    minTrkHits = cms.int32( -1 ),
    previousCandTag = cms.InputTag( "l1tSingleMuon5" ),
    inputMuonCollection = cms.InputTag( "hltPhase2L3Muons" ),
    inputCandCollection = cms.InputTag( "hltPhase2L3MuonCandidates" )
)

process.hltL3fL1TkTripleMu533L31055DZFiltered0p2 = cms.EDFilter( "HLT2MuonMuonDZ",
    saveTags = cms.bool( True ),
    originTag1 = cms.VInputTag( 'hltPhase2L3MuonCandidates' ),
    originTag2 = cms.VInputTag( 'hltPhase2L3MuonCandidates' ),
    MinPixHitsForDZ = cms.int32( 1 ),
    MinN = cms.int32( 3 ),
    triggerType1 = cms.int32( 83 ),
    triggerType2 = cms.int32( 83 ),
    MinDR = cms.double( 0.001 ),
    MaxDZ = cms.double( 0.2 ),
    inputTag1 = cms.InputTag( "hltL3fL1TkTripleMu533PreFiltered555" ),
    checkSC = cms.bool( False ),
    inputTag2 = cms.InputTag( "hltL3fL1TkTripleMu533PreFiltered555" )
)
# -- #

# -- Path and Schedule -- #
process.HLT_IsoMu24FromL1TkMuon = cms.Path(
    process.HLTBeginSequence+

    # L1TkMuon filter
    process.hltL1TkSingleMuFiltered22+

    # local reco
    process.HLTMuonLocalRecoSequence+
    process.HLTDoLocalPixelSequence+
    process.HLTDoLocalStripSequence+

    # L2 + L3 reco
    process.HLTL2muonrecoSequence+
    process.HLTPhase2L3MuonRecoSequence+

    process.hltL3fL1TkSingleMu22L3Filtered24Q+

    # Isolation sequence including filters
    process.HLTPhase2L3MuonIsoSequenceTrkRegionalNew+

    process.HLTEndSequence
)

# N.B. L1 DZ and dR filters are not implemented yet
process.L1_TripleMuon_5_3_3 = cms.Path(
   process.l1tTripleMuon3+
   process.l1tSingleMuon5
)

process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon = cms.Path(
    process.HLTBeginSequence+

    # L1TkMuon filters
    process.l1tTripleMuon3+ 
    process.l1tSingleMuon5+

    # local reco
    process.HLTMuonLocalRecoSequence+
    process.HLTDoLocalPixelSequence+
    process.HLTDoLocalStripSequence+

    # L2 + L3 reco
    process.HLTL2muonrecoSequence+
    process.HLTPhase2L3MuonRecoSequence+

    # L3 filters
    process.hltL3fL1TkTripleMu533PreFiltered555+
    process.hltL3fL1TkTripleMu533L3Filtered1055+
    process.hltL3fL1TkTripleMu533L31055DZFiltered0p2+

    process.HLTEndSequence
)

process.schedule = cms.Schedule(
    process.L1simulation_step,
    # process.HLT_IsoMu24FromL1TkMuon,
    process.L1_TripleMuon_5_3_3,
    process.HLT_TriMu_10_5_5_DZ_FromL1TkMuon,
    process.HLTriggerFinalPath
)
# -- #

# -- Test Setup -- #
process.load( "DQMServices.Core.DQMStore_cfi" )
process.DQMStore.enableMultiThread = True

process.GlobalTag.globaltag = "111X_mcRun4_realistic_T15_v3"

process.source.fileNames = cms.untracked.vstring(

    # "root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTTo2L2Nu_TuneCP5_14TeV-powheg-pythia8/FEVT/NoPU_111X_mcRun4_realistic_T15_v1-v1/130000/2DDCF15E-DE13-5949-98D7-4F4C2B10759C.root",

    "root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/ZH_HToBB_ZInclusive_M125_TuneCUETP8M1_14TeV_powheg_pythia8/FEVT/NoPU_111X_mcRun4_realistic_T15_v1-v1/130000/6B06B794-81DB-3A43-80B0-041BF0E9BF5A.root",

    # "root://xrootd-cms.infn.it//store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/BplusToJpsiK_NoFilter_TuneCP5_14TeV-pythia8-evtgen/GEN-SIM-DIGI-RAW-MINIAOD/NoPU_111X_mcRun4_realistic_T15_v1-v1/260000/90DB40B9-4783-3D40-9685-2513D99BC725.root",

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYJetsToLL_M-10to50_TuneCP5_14TeV-madgraphMLM-pythia8/GEN-SIM-DIGI-RAW-MINIAOD/PU200_111X_mcRun4_realistic_T15_v1-v1/120000/5821E269-9E33-AE49-9133-67A03F2527EC.root",

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7512F92-AA6C-F642-BBA5-8BAED84CF4C9.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F786C6BD-D600-A845-B12B-D2A499B05D2B.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F7CBE904-DE8D-ED4D-A5C3-EACE571910BE.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F8C8FBAC-2360-E649-B7C9-A1F5C8F2A788.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/F9371A50-AC2F-1649-9949-11D1C169E6A5.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAB40CB7-0647-F344-8470-2E0BAB68C7AF.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FAF35BE0-D62E-9E41-AA4E-6EFA98032795.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FB635D0A-F1D3-5D4E-90AD-6C396681FC87.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FC9170CA-633F-EB4C-8CE5-4E2D29969EBB.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FCB6CEBD-0248-1C4E-9C95-D45A3F3F5902.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FDE7E62F-A277-B145-9FC7-8078B21C0913.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/TTToSemiLepton_TuneCP5_14TeV-powheg-pythia8/FEVT/PU200_111X_mcRun4_realistic_T15_v1-v1/270000/FE7B45F1-3D6D-7643-999E-CEA976B2CDC1.root",

    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FC1C5501-17FF-AD4E-B0C2-78B114D94AD6.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD2DCC3C-9732-854B-AD23-A010899DB902.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD35A9AA-051D-B94B-A971-901867BFED51.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FD8D88D6-E791-6B4F-B067-AAFEA3F852D3.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDA9AEB8-5A1F-AF49-B919-5C7A64194B0A.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDB296D7-F051-9645-BC27-9D222B962B3A.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FDBE16F6-13A5-FF48-A316-83D9B8FB3CB2.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE0F2AF9-BDD9-AF4A-88F1-D426E89F788E.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FE352801-A32A-304E-8EF2-FEB62D8A4036.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FEA94BB5-2837-A14F-9F65-24D5103522D2.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF3C16DF-5B11-8B4A-9B67-DF3CEF790F2F.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/FF7BF0E2-1380-2D48-BB19-F79E6907CD5D.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/87C80516-CB14-0346-9579-1CCCE4607148.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0058F613-AE76-4840-82C3-7F6F3224BBF3.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/0064CF05-E335-5440-BDA1-4DDA696F3CBD.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/008A2993-1370-424A-ABA1-B2D163F8AEED.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/012D4B65-425E-8A49-B961-A289D0447E1E.root",
    # "file:/eos/cms/store/mc/Phase2HLTTDRSummer20ReRECOMiniAOD/DYToLL_M-50_TuneCP5_14TeV-pythia8/FEVT/PU200_pilot_111X_mcRun4_realistic_T15_v1-v1/270000/014A3F26-43E6-AA41-B605-AA4861CE6351.root",
)

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32( -1 )
)

process.options = cms.untracked.PSet(
    wantSummary = cms.untracked.bool( True ),
    numberOfThreads = cms.untracked.uint32( 1 ),
    numberOfStreams = cms.untracked.uint32( 0 ),
    sizeOfStackForThreadsInKB = cms.untracked.uint32( 10*1024 )
)

if 'MessageLogger' in process.__dict__:
    process.MessageLogger.categories.append('TriggerSummaryProducerAOD')
    process.MessageLogger.categories.append('L1GtTrigReport')
    process.MessageLogger.categories.append('L1TGlobalSummary')
    process.MessageLogger.categories.append('HLTrigReport')
    process.MessageLogger.categories.append('FastReport')
    process.MessageLogger.cerr.FwkReport.reportEvery = 1  # 1000
# -- #


from SLHCUpgradeSimulations.Configuration.aging import customise_aging_1000
process = customise_aging_1000(process)

from L1Trigger.Configuration.customisePhase2TTNoMC import customisePhase2TTNoMC
process = customisePhase2TTNoMC(process)

from HLTrigger.Configuration.Eras import modifyHLTforEras
modifyHLTforEras(process)


# process.Timing = cms.Service("Timing",
#     summaryOnly = cms.untracked.bool(True),
#     useJobReport = cms.untracked.bool(True)
# )

# process.SimpleMemoryCheck = cms.Service("SimpleMemoryCheck",
#     ignoreTotal = cms.untracked.int32(1)
# )

# print process.dumpPython()

