L1TCaloLayer1LUTWriter
----------------------

Setup instructions:
```bash
cmsrel CMSSW_10_0_0
cd CMSSW_10_0_0/src/
cmsenv
git cms-init
git cms-merge-topic -u cms-l1t-offline:l1t-integration-$CMSSW_VERSION
pushd L1Trigger
git clone git@github.com:uwcms/L1TCaloLayer1LUTWriter.git
popd
scram b -j 8
cd L1Trigger/L1TCaloLayer1LUTWriter/test
```

Example of generating the LUTs:
```bash
cmsRun testL1TCaloLayer1LUTWriter.py caloParams=caloParams_2018_v1_1_inconsistent_cfi
```

Configuration options for `testL1TCaloLayer1LUTWriter.py`:
 * `caloParams`, default: None, set the name of the CaloParams file to use to generate LUTs.  If not specified, CaloParams in the Global Tag will be used.
 * `runNumber`, default: `1`, can be useful to dump LUTs for a particular data run (e.g. check O2O worked as expected)
 * `outputFile`, default: `luts.xml`
 * `saveHcalScaleFile`, default: false, prints the HCAL TP Compression scale to `hcalScale.txt`

You will have to edit `testL1TCaloLayer1LUTWriter.py` to select the Global Tag.
