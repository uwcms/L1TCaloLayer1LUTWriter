import FWCore.ParameterSet.Config as cms

from FWCore.ParameterSet.VarParsing import VarParsing

from Configuration.StandardSequences.Eras import eras
process = cms.Process("L1TCaloLayer1LUTWriter",eras.Run2_2018)

options = VarParsing()
options.register('caloParams', '', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Input CaloParams location')
options.register('runNumber', 1, VarParsing.multiplicity.singleton, VarParsing.varType.int, 'Run to analyze')
options.register('outputFile', 'luts.xml', VarParsing.multiplicity.singleton, VarParsing.varType.string, 'Output XML File')
options.register('saveHcalScaleFile', False, VarParsing.multiplicity.singleton, VarParsing.varType.bool, 'Output HCAL Compression Scale File')
options.parseArguments()

# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')
from Configuration.AlCa.GlobalTag import GlobalTag

process.source = cms.Source('EmptySource',
    firstRun = cms.untracked.uint32(options.runNumber)
)

# Writes LUT for the only event to be processed - ignores data itself.
process.maxEvents = cms.untracked.PSet( input = cms.untracked.int32(1) )

process.load('L1Trigger.L1TCaloLayer1LUTWriter.l1tCaloLayer1LUTWriter_cfi')
process.l1tCaloLayer1LUTWriter.fileName = options.outputFile
process.l1tCaloLayer1LUTWriter.saveHcalScaleFile = options.saveHcalScaleFile
process.p = cms.Path(process.l1tCaloLayer1LUTWriter)
process.schedule = cms.Schedule(process.p)

#
# Things that actually matter start here
#

# See  "L1Trigger/L1TCaloLayer1/src/UCTLayer1.hh" for explanation
process.l1tCaloLayer1LUTWriter.firmwareVersion = 3

# Will affect the HCAL LUTs, and CaloParams if they are ever in GT...
process.GlobalTag = GlobalTag(process.GlobalTag, '123X_mcRun3_2021_realistic_v13', '')


if options.caloParams:
    # To get L1 CaloParams if we don't want what is in the GT
    # (typically true unless checking params of a previous data run)
    process.load('L1Trigger.L1TCalorimeter.'+options.caloParams)

    # These are not yet in CaloParams by default
    from L1Trigger.L1TCaloLayer1LUTWriter.layer1SecondStageLUTs import layer1SecondStageLUT
    process.caloStage2Params.layer1SecondStageLUT = layer1SecondStageLUT


# HCAL Plan1 geometry can be loaded form RecoDB if using a recent enough run number (or a MC global tag)
# Beware that the HCAL compression LUTs ARE RUN DEPENDENT
process.load("Configuration.StandardSequences.GeometryRecoDB_cff")
# These geometry files might be useful if the GT doesn't have what we need in any IOV
# 2016 running used LUTs created with the 'Extended2016' geometry
#process.load('Configuration.Geometry.GeometryExtended2016Reco_cff')
#process.load("Configuration.Geometry.GeometryExtended2017Plan1_cff")
#process.load("Configuration.Geometry.GeometryExtended2017Plan1Reco_cff")


# HF 1x1 TPs need special ES source as of 2016/03/21
# This was used for 2016 LUTs but appears unnecessary as the 1x1 has been
# incorporated in the geometry if an appropriate IOV is given (i.e. run number after 1x1 installed)
# from L1Trigger.Configuration.customiseReEmul import L1TEventSetupForHF1x1TPs
# process = L1TEventSetupForHF1x1TPs(process)


# To get the CaloTPGTranscoder, which decodes the HCAL compression LUT
process.load('SimCalorimetry.HcalTrigPrimProducers.hcaltpdigi_cff')
# From an email by Aleko:
# "For simulation you want LUTGenerationMode=True; (it's about which conditions to use for input LUTs)."
# Not sure what that means...
process.HcalTPGCoderULUT.LUTGenerationMode = cms.bool(True)
