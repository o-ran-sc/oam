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
package org.oransc.oam.features.devicemanager.xran.test;

import static org.junit.Assert.assertTrue;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.io.IOException;
import org.junit.After;
import org.junit.BeforeClass;
import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.DeviceManagerServiceProvider;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.Capabilities;
import org.onap.ccsdk.features.sdnr.wt.netconfnodestateservice.NetconfAccessor;
import org.opendaylight.yang.gen.v1.urn.xran.hardware._1._0.rev180720.XRANRADIO;
import org.opendaylight.yangtools.yang.common.QName;
import org.oransc.oam.features.devicemanager.xran.impl.XRanNetworkElementFactory;
import org.oransc.oam.features.devicemanager.xran.test.mock.NetconfAccessorMock;

public class TestXORanNetworkElementFactory {

    static NetconfAccessor accessor;
    static DeviceManagerServiceProvider serviceProvider;
    static Capabilities capabilities;
    QName qCapability;

    @BeforeClass
    public static void init() throws InterruptedException, IOException {
        capabilities = mock(Capabilities.class);
        accessor = mock(NetconfAccessorMock.class);
        serviceProvider = mock(DeviceManagerServiceProvider.class);

        when(accessor.getCapabilites()).thenReturn(capabilities);
        when(serviceProvider.getDataProvider()).thenReturn(null);
    }

    @Test
    public void testCreateORANHWComponent() throws Exception {
        when(accessor.getCapabilites().isSupportingNamespace(XRANRADIO.QNAME)).thenReturn(true);
        XRanNetworkElementFactory factory = new XRanNetworkElementFactory();
        assertTrue(factory.create(accessor, serviceProvider).isPresent());
    }

    @Test
    public void testCreateNone() throws Exception {
        when(accessor.getCapabilites().isSupportingNamespace(XRANRADIO.QNAME)).thenReturn(false);
        XRanNetworkElementFactory factory = new XRanNetworkElementFactory();
        assertTrue(!factory.create(accessor, serviceProvider).isPresent());
    }

    @After
    public void cleanUp() throws Exception {

    }
}

