/*******************************************************************************
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
 ******************************************************************************/
package org.onap.ccsdk.features.sdnr.wt.devicemanager.xran.impl;

import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.Uuid;

public class NullableHelper {

    private static final @NonNull Uuid DEFAULT_Uuid = new Uuid("ad3545a5-1dd0-4293-b2d9-90366357a032");

    public static @NonNull Uuid nnGetUuid(@Nullable Uuid x) {
         return x == null ? DEFAULT_Uuid : x;
    }

    public static @NonNull Integer nnGetInteger(@Nullable Integer x) {
        return x == null ? -1 : x;
    }

}
