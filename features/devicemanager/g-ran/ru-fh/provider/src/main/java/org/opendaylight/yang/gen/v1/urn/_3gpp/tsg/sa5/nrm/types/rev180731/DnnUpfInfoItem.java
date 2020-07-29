package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping DnnUpfInfoItem {
 *   leaf dnn {
 *     type t_Dnn;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/DnnUpfInfoItem</i>
 *
 */
public interface DnnUpfInfoItem
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("DnnUpfInfoItem");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TDnn</code> <code>dnn</code>, or <code>null</code> if not present
     */
    @Nullable TDnn getDnn();

}

