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

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.dataprovider.model.DataProvider;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.oransc.oam.features.devicemanager.gran.GRanNetworkElement;

public class TestGRanNetworkElement {

    private static final String NODEID = "node1";

    @Test
    public void test() {
        NetconfAccessor netconfAccessor = mock(NetconfAccessor.class);
        DataProvider databaseService = mock(DataProvider.class);

        when(netconfAccessor.getNodeId()).thenReturn(new NodeId(NODEID));

        GRanNetworkElement gRanNe = new GRanNetworkElement(netconfAccessor, databaseService);
        assertEquals(3, gRanNe.getDeviceType().getIntValue());
        assertEquals("RAN3GPP", gRanNe.getDeviceType().getName());
        assertEquals(NODEID, gRanNe.getNodeId().getValue());

        gRanNe.register();
        gRanNe.deregister();
        gRanNe.warmstart();
        gRanNe.getAcessor();
        gRanNe.getService(null);

    }


}
