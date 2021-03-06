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
package org.oransc.oam.features.devicemanager.xran.impl;

import org.opendaylight.yang.gen.v1.urn.xran.fm._1._0.rev180720.AlarmNotif;
import org.opendaylight.yang.gen.v1.urn.xran.fm._1._0.rev180720.XranFmListener;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;

public class XRanFaultNotificationListener implements XranFmListener {

    private static final Logger log = LoggerFactory.getLogger(XRanFaultNotificationListener.class);

    @Override
    public void onAlarmNotif(AlarmNotif notification) {

        log.info("onAlarmNotif {}", notification);
    }

}
