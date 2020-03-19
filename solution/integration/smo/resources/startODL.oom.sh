#!/bin/bash

###
# ============LICENSE_START=======================================================
# SDNC
# ================================================================================
# Copyright (C) 2017 AT&T Intellectual Property. All rights reserved.
# ================================================================================
# Update by Copyright (C) 2020 highstreet technologies GmbH. All rights reserved.
# ================================================================================
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ============LICENSE_END=========================================================
###
# from helm oom resource file
# Install SDN-C platform components if not already installed and start container

# List of used constants, that are provided during container initialization

ODL_HOME=${ODL_HOME:-/opt/opendaylight/current}
ODL_ADMIN_USERNAME=${ODL_ADMIN_USERNAME:-admin}
ODL_ADMIN_PASSWORD=${ODL_ADMIN_PASSWORD:-Kp8bJ4SXszM0WXlhak3eHlcse2gAw84vaoGGmJvUy2U}
export ODL_ADMIN_PASSWORD ODL_ADMIN_USERNAME

SDNC_HOME=${SDNC_HOME:-/opt/onap/sdnc}
SDNC_BIN=${SDNC_BIN:-/opt/onap/sdnc/bin}
CCSDK_HOME=${CCSDK_HOME:-/opt/onap/ccsdk}

#- ODL Cluster
ENABLE_ODL_CLUSTER=${ENABLE_ODL_CLUSTER:-false}
#SDNC_REPLICAS

#- ODL GEO cluster
GEO_ENABLED=${GEO_ENABLED:-false}
#IS_PRIMARY_CLUSTER
#MY_ODL_CLUSTER
#PEER_ODL_CLUSTER

#- AAF
SDNC_AAF_ENABLED=${SDNC_AAF_ENABLED:-false}

#- SDN-R
SDNRWT=${SDNRWT:-false}
SDNRWT_BOOTFEATURES=${SDNRWT_BOOTFEATURES:-sdnr-wt-feature-aggregator}
SDNRDM=${SDNRDM:-false}
SDNRDM_BOOTFEATURES=${SDNRDM_BOOTFEATURES:-sdnr-wt-feature-aggregator-devicemanager}
SDNRONLY=${SDNRONLY:-false}

SDNRINIT=${SDNRINIT:-false}
SDNRDBURL=${SDNRDBURL:-http://sdnrdb:9200}
#SDNRDBUSERNAME
#SDNRDBPASSWORD
#SDNRDBPARAMETER
SDNRDBCOMMAND=${SDNRDBCOMMAND:--c init -db $SDNRDBURL -dbu $SDNRDBUSERNAME -dbp $SDNRDBPASSWORD $SDNRDBPARAMETER}

SDNR_NORTHBOUND=${SDNR_NORTHBOUND:-false}
SDNR_NORTHBOUND_BOOTFEATURES=${SDNR_NORTHBOUND_BOOTFEATURES:-sdnr-northbound-all}

# Functions

# Append features to karaf boot feature configuration
# $1 additional feature to be added
# $2 repositories to be added (optional)
function addToFeatureBoot() {
  CFG=$ODL_HOME/etc/org.apache.karaf.features.cfg
  ORIG=$CFG.orig
  if [ -n "$2" ] ; then
    echo "Add repository: $2"
    mv $CFG $ORIG
    cat $ORIG | sed -e "\|featuresRepositories|s|$|,$2|" > $CFG
  fi
  echo "Add boot feature: $1"
  mv $CFG $ORIG
  cat $ORIG | sed -e "\|featuresBoot *=|s|$|,$1|" > $CFG
}

# Append features to karaf boot feature configuration
# $1 search pattern
# $2 replacement
function replaceFeatureBoot() {
  CFG=$ODL_HOME/etc/org.apache.karaf.features.cfg
  ORIG=$CFG.orig
  echo "Replace boot feature $1 with: $2"
  sed -i "/featuresBoot/ s/$1/$2/g" $CFG
}

# Remove features from karaf boot feature configuration
# $1 search pattern
function removeFeatureBoot() {
  CFG=$ODL_HOME/etc/org.apache.karaf.features.cfg
  ORIG=$CFG.orig
  echo "Remove boot feature $1"
  sed -i "/featuresBoot/ s/,\s*$1//g" $CFG
}


function initialize_sdnr() {
  echo "SDN-R Database Initialization"
  INITCMD="$JAVA_HOME/bin/java -jar "
  INITCMD+="$ODL_HOME/system/org/onap/ccsdk/features/sdnr/wt/sdnr-wt-data-provider-setup/$CCSDKFEATUREVERSION/sdnr-dmt.jar "
  INITCMD+="$SDNRDBCOMMAND"
  echo "Execute: $INITCMD"
  n=0
  until [ $n -ge 5 ]
  do
    $INITCMD && break
    n=$[$n+1]
    sleep 15
  done
  return $?
}

function install_sdnrwt_features() {
  # Repository setup provided via sdnc dockerfile
  if $SDNRWT; then
    #if $SDNRONLY; then
    #  RUN sed -i -e /featuresBoot/d $ODL_HOME/etc/org.apache.karaf.features.cfg
    #  RUN echo featuresBoot=config,standard,region,package,kar,ssh,management,odl-mdsal-all,odl-mdsal-apidocs,odl-daexim-all,odl-netconf-topology >> $ODL_HOME/etc/org.apache.karaf.features.cfg
    #fi
    if $SDNRDM; then
      addToFeatureBoot "$SDNRDM_BOOTFEATURES"
    else
      addToFeatureBoot "$SDNRWT_BOOTFEATURES"
    fi
    if $SDNRONLY; then
      removeFeatureBoot ccsdk-sli-core-all
      removeFeatureBoot ccsdk-sli-adaptors-all
      removeFeatureBoot ccsdk-sli-northbound-all
      removeFeatureBoot ccsdk-sli-plugins-all
      removeFeatureBoot ccsdk-features-all
      removeFeatureBoot sdnc-northbound-all
      removeFeatureBoot sdnr-northbound-all
    fi
  fi
}

function install_sdnr_northbound_features() {
  # Repository setup provided via sdnc dockerfile
  addToFeatureBoot "$SDNR_NORTHBOUND_BOOTFEATURES"
}

# Reconfigure ODL from default single node configuration to cluster

function enable_odl_cluster(){
  if [ -z $SDNC_REPLICAS ]; then
     echo "SDNC_REPLICAS is not configured in Env field"
     exit
  fi

  # ODL NETCONF setup
  echo "Installing Opendaylight cluster features for mdsal and netconf"

  #Be sure to remove feature odl-netconf-connector-all from list
  replaceFeatureBoot "odl-netconf-connector-all,"
  #Activate cluster
  replaceFeatureBoot odl-netconf-topology odl-netconf-clustered-topology
  replaceFeatureBoot odl-mdsal-all odl-mdsal-all,odl-mdsal-clustering
  addToFeatureBoot odl-jolokia

  # ODL Cluster or Geo cluster configuration

  echo "Update cluster information statically"
  fqdn=$(hostname -f)
  echo "Get current fqdn ${fqdn}"

  # Extract node index using first digit after "-"
  # Example 2 from "sdnr-2.logo.ost.das.r32.com"
  node_index=($(echo ${fqdn} | sed -r 's/.*-([0-9]).*/\1/g'))

  if $GEO_ENABLED; then
    echo "This is a Geo cluster"

    if [ -z $IS_PRIMARY_CLUSTER ] || [ -z $MY_ODL_CLUSTER ] || [ -z $PEER_ODL_CLUSTER ]; then
     echo "IS_PRIMARY_CLUSTER, MY_ODL_CLUSTER and PEER_ODL_CLUSTER must all be configured in Env field"
     return
    fi

    member_offset=1
    if $IS_PRIMARY_CLUSTER; then
       PRIMARY_NODE=${MY_ODL_CLUSTER}
       SECONDARY_NODE=${PEER_ODL_CLUSTER}
    else
       PRIMARY_NODE=${PEER_ODL_CLUSTER}
       SECONDARY_NODE=${MY_ODL_CLUSTER}
       member_offset=4
    fi

    node_list="${PRIMARY_NODE} ${SECONDARY_NODE}"
    $SDNC_BIN/configure_geo_cluster.sh $((node_index+member_offset)) ${node_list}
  else
    echo "This is a local cluster"
    for ((i=0;i<${SDNC_REPLICAS};i++)); do
      #assemble node list by replaceing node-index in hostname with "i"
      node_name=$(echo ${fqdn} | sed -r "s/-[0-9]/-$i/g")
      node_list="${node_list} $node_name"
    done
    echo "Node index: $((node_index+1)) list: ${node_list[@]}"
    $ODL_HOME/bin/configure_cluster.sh $((node_index+1)) ${node_list}
  fi
}

# -----------------------
# Main script starts here

echo "Settings:"
echo "  ENABLE_ODL_CLUSTER=$ENABLE_ODL_CLUSTER"
echo "  SDNC_REPLICAS=$SDNC_REPLICAS"
echo "  CCSDKFEATUREVERSION=$CCSDKFEATUREVERSION"
echo "  SDNR_NORTHBOUND=$SDNR_NORTHBOUND"
echo "  SDNRWT=$SDNRWT"
echo "  SDNRDM=$SDNRDM"
echo "  SDNRONLY=$SDNRONLY"
echo "  SDNRINIT=$SDNRINIT"
echo "  SDNRDBURL=$SDNRDBURL"
echo "  SDNRDBUSERNAME=$SDNRDBUSERNAME"
echo "  SDNRDBPASSWORD=$SDNRDBPASSWORD"
echo "  GEO_ENABLED=$GEO_ENABLED"
echo "  IS_PRIMARY_CLUSTER=$IS_PRIMARY_CLUSTER"
echo "  MY_ODL_CLUSTER=$MY_ODL_CLUSTER"
echo "  PEER_ODL_CLUSTER=$PEER_ODL_CLUSTER"
echo "  AAF_ENABLED=$SDNC_AAF_ENABLED"


if $SDNC_AAF_ENABLED; then
    export SDNC_STORE_DIR=/opt/app/osaaf/local
    export SDNC_CONFIG_DIR=/opt/app/osaaf/local
    export SDNC_KEYPASS=`cat /opt/app/osaaf/local/.pass`
    export SDNC_KEYSTORE=org.onap.sdnc.p12
    sed -i '/cadi_prop_files/d' $ODL_HOME/etc/system.properties
    echo "cadi_prop_files=$SDNC_CONFIG_DIR/org.onap.sdnc.props" >> $ODL_HOME/etc/system.properties

    sed -i '/org.ops4j.pax.web.ssl.keystore/d' $ODL_HOME/etc/custom.properties
    sed -i '/org.ops4j.pax.web.ssl.password/d' $ODL_HOME/etc/custom.properties
    sed -i '/org.ops4j.pax.web.ssl.keypassword/d' $ODL_HOME/etc/custom.properties
    echo org.ops4j.pax.web.ssl.keystore=$SDNC_STORE_DIR/$SDNC_KEYSTORE >> $ODL_HOME/etc/custom.properties
    echo org.ops4j.pax.web.ssl.password=$SDNC_KEYPASS >> $ODL_HOME/etc/custom.properties
    echo org.ops4j.pax.web.ssl.keypassword=$SDNC_KEYPASS >> $ODL_HOME/etc/custom.properties
fi

if $SDNRINIT ; then
  #One time intialization action
  initialize_sdnr
  init_result=$?
  echo "Result of init script: $init_result"
  #exit $init_result
fi

if [ ! -f ${SDNC_HOME}/.installed ]
then
    echo "Installing SDN-C keyStore"
    /bin/bash ${SDNC_HOME}/bin/addSdncKeyStore.sh

    if $ENABLE_ODL_CLUSTER ; then enable_odl_cluster ; fi

    if $SDNRWT ; then install_sdnrwt_features ; fi

    if $SDNR_NORTHBOUND ; then install_sdnr_northbound_features ; fi

    echo "Installed at `date`" > ${SDNC_HOME}/.installed
fi

if [ -d /opt/opendaylight/current/certs ] ; then
  cp /opt/opendaylight/current/certs/* /tmp
fi
nohup python ${SDNC_BIN}/installCerts.py &

exec ${ODL_HOME}/bin/karaf server

