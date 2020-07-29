package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.util.List;
import org.eclipse.jdt.annotation.NonNull;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.snssaiupfinfoitem.DnnUpfInfo;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping SnssaiUpfInfoItem {
 *   leaf sNssai {
 *     type t_s-NSSAI;
 *   }
 *   list dnnUpfInfo {
 *     key dnn;
 *     uses DnnUpfInfoItem;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/SnssaiUpfInfoItem</i>
 *
 */
public interface SnssaiUpfInfoItem
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("SnssaiUpfInfoItem");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TSNSSAI</code> <code>sNssai</code>, or <code>null</code> if not present
     */
    @Nullable TSNSSAI getSNssai();
    
    /**
     * @return <code>java.util.List</code> <code>dnnUpfInfo</code>, or <code>null</code> if not present
     */
    @Nullable List<DnnUpfInfo> getDnnUpfInfo();
    
    /**
     * @return <code>java.util.List</code> <code>dnnUpfInfo</code>, or an empty list if it is not present
     */
    default @NonNull List<DnnUpfInfo> nonnullDnnUpfInfo() {
        return CodeHelpers.nonnull(getDnnUpfInfo());
    }

}

