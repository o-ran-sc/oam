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
package org.onap.ccsdk.features.sdnr.wt.devicemanager.oran.test;

import static org.junit.Assert.assertEquals;
import static org.mockito.Mockito.mock;
import static org.mockito.Mockito.when;

import java.util.List;
import java.util.Optional;
import java.io.IOException;
import java.util.ArrayList;

import org.eclipse.jdt.annotation.Nullable;
import org.junit.After;
import org.junit.Before;
import org.junit.Test;
import org.mockito.Mockito;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.iana.hardware.rev180313.HardwareClass;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.hardware.rev180313.hardware.Component;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.DateAndTime;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.Uuid;
import org.opendaylight.yang.gen.v1.urn.tbd.params.xml.ns.yang.network.topology.rev131021.NodeId;
import org.oransc.oam.features.devicemanager.oran.impl.ORanToInternalDataModel;
import org.onap.ccsdk.features.sdnr.wt.devicemanager.oran.test.TestHardwareClass;

public class TestORanToInternalDataModel {

	NodeId nodeId;
	Component component;

	@SuppressWarnings("unchecked")
	@Before
	public void init() throws InterruptedException, IOException {
		nodeId = mock(NodeId.class);
		component = mock(Component.class);

		when(nodeId.getValue()).thenReturn("ORan-1000");
		when(component.getParent()).thenReturn("Shelf");
		when(component.getParentRelPos()).thenReturn(0);
		when(component.getUuid()).thenReturn(new Uuid("0Aabcdef-0abc-0cfD-0abC-0123456789AB"));

		List<String> list = new ArrayList<String>();
		list.add("Card-01A");
		list.add("Card-01B");

		when (component.getContainsChild()).thenReturn(list);
		when (component.getName()).thenReturn("Nokia");
		when (component.getDescription()).thenReturn("ORAN Network Element NO-456");
		Class<? extends HardwareClass> hwClass = TestHardwareClass.class;
		Mockito.<Class<? extends HardwareClass>>when(component.getXmlClass()).thenReturn(hwClass);
		
		DateAndTime dt = new DateAndTime("2020-02-05T12:30:45.283Z");
		when (component.getMfgDate()).thenReturn(dt);
		
	}

	@Test
	public void test() throws Exception {
		ORanToInternalDataModel model = new ORanToInternalDataModel();
		model.getInternalEquipment(nodeId, component);
		assertEquals(component.getUuid().getValue(), "0Aabcdef-0abc-0cfD-0abC-0123456789AB");
		assertEquals(component.getMfgDate().getValue(), "2020-02-05T12:30:45.283Z");

	}

	@After
	public void cleanUp() throws Exception {

	}
}
