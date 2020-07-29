package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.tai.PlmnId;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping Tai {
 *   container plmnId {
 *     uses pLMNId;
 *   }
 *   leaf tac {
 *     type t_tAC;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Tai</i>
 *
 */
public interface Tai
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("Tai");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.tai.PlmnId</code> <code>plmnId</code>, or <code>null</code> if not present
     */
    @Nullable PlmnId getPlmnId();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TTAC</code> <code>tac</code>, or <code>null</code> if not present
     */
    @Nullable TTAC getTac();

}

