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
package org.onap.ccsdk.features.sdnr.wt.devicemanager.xran;

import static org.junit.Assert.assertEquals;
import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;
import static org.mockito.Mockito.*;

import java.util.Optional;
import java.io.IOException;
import org.junit.After;
import org.junit.BeforeClass;
import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.dataprovider.model.DataProvider;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.ne.service.NetworkElement;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.opendaylight.yang.gen.v1.urn.xran.hardware._1._0.rev180720.XRANRADIO;
import org.opendaylight.yangtools.yang.common.QName;
import org.oransc.oam.features.devicemanager.xran.impl.XRanNetworkElementFactory;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.xran.mock.NetconfAccessorMock;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.xran.mock.TransactionUtilsMock;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.Capabilities;

public class TestXRanNetworkElement {

    static NetconfAccessorMock accessor;
    static DeviceManagerServiceProvider serviceProvider;
    static Capabilities capabilities;
    QName qCapability;

    @BeforeClass
    public static void init() throws InterruptedException, IOException {
        capabilities = mock(Capabilities.class);
        //accessor = mock(NetconfAccessorMock.class);
        accessor = spy(new NetconfAccessorMock(null, null, null, null));
        serviceProvider = mock(DeviceManagerServiceProvider.class);

        NodeId nNodeId = new NodeId("nSky");
        when(accessor.getCapabilites()).thenReturn(capabilities);
        when (accessor.getNodeId()).thenReturn(nNodeId);
        when (accessor.getTransactionUtils()).thenReturn(new TransactionUtilsMock());

        DataProvider dataProvider = mock(DataProvider.class);
        when(serviceProvider.getDataProvider()).thenReturn(dataProvider);
    }

    @Test
    public void test() {
        Optional<NetworkElement> oRanNe;
        when(accessor.getCapabilites().isSupportingNamespace(XRANRADIO.QNAME)).thenReturn(true);
        XRanNetworkElementFactory factory = new XRanNetworkElementFactory();
        oRanNe = factory.create(accessor, serviceProvider);
        assertTrue(factory.create(accessor, serviceProvider).isPresent());
        oRanNe.get().register();
        oRanNe.get().deregister();
        oRanNe.get().getAcessor();
        oRanNe.get().getDeviceType();
        assertEquals(oRanNe.get().getNodeId().getValue(), "nSky");
    }

    @After
    public void cleanUp() throws Exception {

    }
}
