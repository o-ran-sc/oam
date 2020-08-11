package org.oransc.oam.features.devicemanager.xran.test;

import java.io.File;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.oransc.oam.features.devicemanager.xran.impl.DeviceManagerXRanImpl;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class TestDeviceManagerXRanImpl {
    private static Path KARAF_ETC = Paths.get("etc");
    private static final Logger LOG = LoggerFactory.getLogger(TestDeviceManagerXRanImpl.class);
    DeviceManagerXRanImpl devMgrXran;

    @Before
    public void init() throws InterruptedException, IOException {
        /*System.out.println("Logger: " + LOG.getClass().getName() + " " + LOG.getName());
        Path etc = KARAF_ETC;
        delete(etc);

        System.out.println("Create empty:" + etc.toString());
        Files.createDirectories(etc);*/
    }

    @Test
    public void test() throws Exception {
        devMgrXran = new DeviceManagerXRanImpl();
        /*DeviceManagerImpl devMgr = new DeviceManagerImpl();

        try {
            devMgr.init();
            devMgrOran.setNetconfNetworkElementService(devMgr);
            devMgrOran.init();
        } catch (Exception e) {
            // TODO Auto-generated catch block
            e.printStackTrace();
        }*/
        /*
         * devMgrOran.setNetconfNetworkElementService(null); devMgrOran.init();
         * NetconfNetworkElementService netConfNetworkElementService =
         * mock(NetconfNetworkElementService.class); devMgrOran =
         * mock(DeviceManagerORanImpl.class);
         * when(netConfNetworkElementService.registerNetworkElementFactory(new
         * ORanNetworkElementFactory())).thenReturn(null);
         */


    }

    @After
    public void cleanUp() throws Exception {
            devMgrXran.close();
    }

    private static void delete(Path etc) throws IOException {
        if (Files.exists(etc)) {
            System.out.println("Found, removing:" + etc.toString());
            delete(etc.toFile());
        }
    }

    private static void delete(File f) throws IOException {
        if (f.isDirectory()) {
            for (File c : f.listFiles()) {
                delete(c);
            }
        }
        if (!f.delete()) {
            throw new FileNotFoundException("Failed to delete file: " + f);
        }
    }
}
