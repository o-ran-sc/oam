# 3gpp Release 16 

This folder should contain the 3GPP YAML files. Such files are used be the VES
Collector to valid VES messages for domain 'stndDefined'.

Please copy the files from 
```
https://forge.3gpp.org/rep/sa5/MnS/tree/Rel-16/OpenAPI
```

For E-Release only the following schemas ...

 * comDefs.yaml
 * faultMnS.yaml
 * fileDataReportingMnS.yaml
 * heartbeatNtf.yaml
 * perfMnS.yaml
 * provMnS.yaml

.. are supported.

Therefore the references (dependencies) in the file 'provMnS.yaml' to other schemas must be commanded, otherwise the schema itself would invalid.

# Temporary modification for E-Release in 'provMnS.yaml'

In this release only a subset of 3GPP Release 16 schema are supported. References to non supported schemas should be commanded, until those are supported.

```
developer @ localhost ~/workspace/_3gpp/MnS/OpenAPI (Rel-16)
└─ $ ▶ git diff .
diff --git a/OpenAPI/provMnS.yaml b/OpenAPI/provMnS.yaml
index 1dd467e..699bdce 100644
--- a/OpenAPI/provMnS.yaml
+++ b/OpenAPI/provMnS.yaml
@@ -412,11 +412,11 @@ components:
             type: array
             items:
               type: object
-        - anyOf:
-            - $ref: 'genericNrm.yaml#/components/schemas/resources-genericNrm'
-            - $ref: 'nrNrm.yaml#/components/schemas/resources-nrNrm'
-            - $ref: '5gcNrm.yaml#/components/schemas/resources-5gcNrm'
-            - $ref: 'sliceNrm.yaml#/components/schemas/resources-sliceNrm'
+        # - anyOf:
+        #     - $ref: 'genericNrm.yaml#/components/schemas/resources-genericNrm'
+        #     - $ref: 'nrNrm.yaml#/components/schemas/resources-nrNrm'
+        #     - $ref: '5gcNrm.yaml#/components/schemas/resources-5gcNrm'
+        #     - $ref: 'sliceNrm.yaml#/components/schemas/resources-sliceNrm'
 
     MoiChange:
       type: object
```
