/*
 * ============LICENSE_START========================================================================
 * O-RAN-SC : oam/ccsdk feature sdnr wt
 * =================================================================================================
 * Copyright (C) 2020 highstreet technologies GmbH Intellectual Property. All rights reserved.
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
package org.oransc.oam.features.devicemanager.oran.impl;

import org.onap.ccsdk.features.sdnr.wt.common.database.HtDatabaseClient;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.factory.FactoryRegistration;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.NetconfNetworkElementService;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class DeviceManagerORanImpl implements AutoCloseable {

    private static final Logger LOG = LoggerFactory.getLogger(DeviceManagerORanImpl.class);
    private static final String APPLICATION_NAME = "DeviceManagerORan";
    @SuppressWarnings("unused")
    private static final String CONFIGURATIONFILE = "etc/devicemanager-oran.properties";


    private NetconfNetworkElementService netconfNetworkElementService;

    private HtDatabaseClient htDatabaseClient;
    private Boolean devicemanagerInitializationOk = false;
    private FactoryRegistration<ORanNetworkElementFactory> resORan;

    // Blueprint begin
    public DeviceManagerORanImpl() {
        LOG.info("Creating provider for {}", APPLICATION_NAME);
        resORan = null;
    }

    public void setNetconfNetworkElementService(NetconfNetworkElementService netconfNetworkElementService) {
        this.netconfNetworkElementService = netconfNetworkElementService;
    }

    public void init() throws Exception {

        LOG.info("Session Initiated start {}", APPLICATION_NAME);

        resORan = netconfNetworkElementService.registerNetworkElementFactory(new ORanNetworkElementFactory());


        netconfNetworkElementService.writeToEventLog(APPLICATION_NAME, "startup", "done");
        this.devicemanagerInitializationOk = true;

        LOG.info("Session Initiated end. Initialization done {}", devicemanagerInitializationOk);
    }
    // Blueprint end

    @Override
    public void close() throws Exception {
        LOG.info("closing ...");
        close(htDatabaseClient);
        close(resORan);
        LOG.info("closing done");
    }

    /**
     * Used to close all Services, that should support AutoCloseable Pattern
     *
     * @param toClose
     * @throws Exception
     */
    private void close(AutoCloseable... toCloseList) {
        for (AutoCloseable element : toCloseList) {
            if (element != null) {
                try {
                    element.close();
                } catch (Exception e) {
                    LOG.warn("Fail during close: ", e);
                }
            }
        }
    }
}
