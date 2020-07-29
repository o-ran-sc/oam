/*
 * ============LICENSE_START========================================================================
 * ONAP : ccsdk feature sdnr wt
 * =================================================================================================
 * Copyright (C) 2019 highstreet technologies GmbH Intellectual Property. All rights reserved.
 * =================================================================================================
 * Licensed under the Apache License, Version 2.0 (the "License"); you may not use this file except
 * in compliance with the License. You may obtain a copy of the License at
 *
 * http://www.apache.org/licenses/LICENSE-2.0
 *
 * Unless required by applicable law or agreed to in writing, software distributed under the License
 * is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express
 * or implied. See the License for the specific language governing permissions and limitations under
 * the License.
 * ============LICENSE_END==========================================================================
 */
package org.oransc.oam.features.devicemanager.gran.impl;

import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.factory.FactoryRegistration;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.NetconfNetworkElementService;
import org.oransc.oam.features.devicemanager.gran.GRanNetworkElementFactory;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DeviceManagerGRanImpl implements AutoCloseable  {

    private static final Logger LOG = LoggerFactory.getLogger(DeviceManagerGRanImpl.class);
    private static final String APPLICATION_NAME = "DeviceManagerGRan";
    
    private NetconfNetworkElementService netconfNetworkElementService;

    private Boolean devicemanagerInitializationOk;
    private FactoryRegistration<GRanNetworkElementFactory> factoryRegistration;

    // Blueprint 1
    public DeviceManagerGRanImpl() {
        LOG.info("Creating provider for {}", APPLICATION_NAME);
        devicemanagerInitializationOk = false;

        netconfNetworkElementService = null;
        factoryRegistration = null;
    
    }
   public void setNetconfNetworkElementService(NetconfNetworkElementService netconfNetworkElementService) {
       this.netconfNetworkElementService = netconfNetworkElementService;
   }

    public void init() throws Exception {

        LOG.info("Session Initiated start {}", APPLICATION_NAME);
        // Intialization
        factoryRegistration = netconfNetworkElementService.registerNetworkElementFactory(new GRanNetworkElementFactory());
        netconfNetworkElementService.writeToEventLog(APPLICATION_NAME, "startup", "done");
        this.devicemanagerInitializationOk = true;

        LOG.info("Session Initiated end. Initialization done {}", devicemanagerInitializationOk);
    }

    @Override
    public void close() throws Exception {
        LOG.info("closing ...");
        if (factoryRegistration != null) {
            factoryRegistration.close();
        }
        LOG.info("closing done");
    }

}
