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
package org.oransc.oam.features.devicemanager.oran.test;

import org.junit.Test;
import org.oransc.oam.features.devicemanager.oran.impl.ORanFaultNotificationListener;

public class TestORanFaultNotificationListener {

	@Test
	public void test() {
		ORanFaultNotificationListener faultListener = new ORanFaultNotificationListener();
		faultListener.onAlarmNotif(null);
	}
}
