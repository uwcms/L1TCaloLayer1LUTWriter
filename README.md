L1TCaloLayer1LUTWriter
----------------------

Setup instructions:
```bash
cmsrel CMSSW_9_3_0_pre3
cd CMSSW_9_3_0_pre3/src/
cmsenv
git cms-init
git cms-addpkg L1Trigger/L1TCaloLayer1
git cms-merge-topic -u 19875
git cms-merge-topic -u 20000
cd L1Trigger
git clone git@github.com:uwcms/L1TCaloLayer1LUTWriter.git
cd ..
scram b -j 8
cd L1Trigger/L1TCaloLayer1LUTWriter/test
```

Generating the LUTs:
```bash
cmsRun testL1TCaloLayer1LUTWriter.py
```

Configuration options for `testL1TCaloLayer1LUTWriter.py`:
 * `runNumber`, default: `1`, can be useful to dump LUTs for a particular data run (e.g. check O2O worked as expected)
 * `outputFile`, default: `luts.xml`
 * `saveHcalScaleFile`, default: false, prints the infamous HCAL TP Compression scale to `hcalScale.txt`

