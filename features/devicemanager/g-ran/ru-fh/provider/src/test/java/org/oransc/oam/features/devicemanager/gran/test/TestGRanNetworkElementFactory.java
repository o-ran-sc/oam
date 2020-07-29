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

import static org.junit.Assert.*;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.Before;
import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.Capabilities;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.top.rev180731.TopGrp;
import org.oransc.oam.features.devicemanager.gran.GRanNetworkElementFactory;


public class TestGRanNetworkElementFactory {

    Capabilities capabilities;
    NetconfAccessor netconfAccessor;
    DeviceManagerServiceProvider devMgrService;

    @SuppressWarnings("unused")
    @Before
    public void init() {
        capabilities = mock(Capabilities.class);
        netconfAccessor = mock(NetconfAccessor.class);
        devMgrService = mock(DeviceManagerServiceProvider.class);

        when(netconfAccessor.getCapabilites()).thenReturn(capabilities);
        when(devMgrService.getDataProvider()).thenReturn(null);

    }

    @Test
    public void testCreate() throws Exception {
        when(netconfAccessor.getCapabilites().isSupportingNamespace(TopGrp.QNAME)).thenReturn(true);

        GRanNetworkElementFactory gRanNeFactory = new GRanNetworkElementFactory();
        assertTrue((gRanNeFactory.create(netconfAccessor, devMgrService)).isPresent());
    }

    @Test
    public void testCreateNone() throws Exception {
        when(netconfAccessor.getCapabilites().isSupportingNamespace(TopGrp.QNAME)).thenReturn(false);

        GRanNetworkElementFactory gRanNeFactory = new GRanNetworkElementFactory();
        assertTrue(!(gRanNeFactory.create(netconfAccessor, devMgrService).isPresent()));
    }

}
