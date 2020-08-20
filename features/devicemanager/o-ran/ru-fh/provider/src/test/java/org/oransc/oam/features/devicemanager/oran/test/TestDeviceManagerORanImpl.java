package org.oransc.oam.features.devicemanager.oran.test;

import static org.mockito.Mockito.mock;
import java.io.IOException;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.service.NetconfNetworkElementService;
import org.oransc.oam.features.devicemanager.oran.impl.DeviceManagerORanImpl;

public class TestDeviceManagerORanImpl {
    DeviceManagerORanImpl devMgrOran;

    @Before
    public void init() throws InterruptedException, IOException {
    }

    @Test
    public void test() throws Exception {
        devMgrOran = new DeviceManagerORanImpl();
        NetconfNetworkElementService netconfNetworkElementService = mock(NetconfNetworkElementService.class);

        try {
            devMgrOran.setNetconfNetworkElementService(netconfNetworkElementService);
            devMgrOran.init();
        } catch (Exception e) {
            throw e;
        }
    }

    @After
    public void cleanUp() throws Exception {
        devMgrOran.close();
    }
}
