/*
 * ============LICENSE_START========================================================================
 * ONAP : ccsdk feature sdnr wt
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
package org.oransc.oam.features.devicemanager.gran.test;

import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.NetconfNetworkElementService;
import org.oransc.oam.features.devicemanager.gran.GRanNetworkElementFactory;
import org.oransc.oam.features.devicemanager.gran.impl.DeviceManagerGRanImpl;

public class TestDeviceManagerGRanImpl {
    GRanNetworkElementFactory factory = new GRanNetworkElementFactory();
    DeviceManagerServiceProvider serviceProvider;

    @Test
    public void test() throws Exception {
        serviceProvider = mock(DeviceManagerServiceProvider.class);
        NetconfNetworkElementService netconfNetworkElementService = mock(NetconfNetworkElementService.class);
        when(netconfNetworkElementService.registerNetworkElementFactory(factory)).thenReturn(null);
        when(netconfNetworkElementService.getServiceProvider()).thenReturn(serviceProvider);

        DeviceManagerGRanImpl devMgrGRan = new DeviceManagerGRanImpl();

        devMgrGRan.setNetconfNetworkElementService(netconfNetworkElementService);
        devMgrGRan.init();
        devMgrGRan.close();

    }

}
