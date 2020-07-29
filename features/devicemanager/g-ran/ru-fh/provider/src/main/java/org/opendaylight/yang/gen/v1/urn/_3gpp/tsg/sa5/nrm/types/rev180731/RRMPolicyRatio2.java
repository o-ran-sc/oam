package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.lang.Integer;
import java.lang.Short;
import java.util.List;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping RRMPolicyRatio2 {
 *   leaf groupId {
 *     type uint16;
 *   }
 *   leaf-list sNSSAI {
 *     type t_s-NSSAI;
 *   }
 *   leaf quotaType {
 *     type t_quotaType;
 *   }
 *   leaf rRMPolicyMaxRation {
 *     type uint8;
 *   }
 *   leaf rRMPolicyMarginMaxRation {
 *     type uint8;
 *   }
 *   leaf rRMPolicyMinRation {
 *     type uint8;
 *   }
 *   leaf rRMPolicyMarginMinRation {
 *     type uint8;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/RRMPolicyRatio2</i>
 *
 */
public interface RRMPolicyRatio2
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("RRMPolicyRatio2");

    /**
     * @return <code>java.lang.Integer</code> <code>groupId</code>, or <code>null</code> if not present
     */
    @Nullable Integer getGroupId();
    
    /**
     * @return <code>java.util.List</code> <code>sNSSAI</code>, or <code>null</code> if not present
     */
    @Nullable List<TSNSSAI> getSNSSAI();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TQuotaType</code> <code>quotaType</code>, or <code>null</code> if not present
     */
    @Nullable TQuotaType getQuotaType();
    
    /**
     * @return <code>java.lang.Short</code> <code>rRMPolicyMaxRation</code>, or <code>null</code> if not present
     */
    @Nullable Short getRRMPolicyMaxRation();
    
    /**
     * @return <code>java.lang.Short</code> <code>rRMPolicyMarginMaxRation</code>, or <code>null</code> if not present
     */
    @Nullable Short getRRMPolicyMarginMaxRation();
    
    /**
     * @return <code>java.lang.Short</code> <code>rRMPolicyMinRation</code>, or <code>null</code> if not present
     */
    @Nullable Short getRRMPolicyMinRation();
    
    /**
     * @return <code>java.lang.Short</code> <code>rRMPolicyMarginMinRation</code>, or <code>null</code> if not present
     */
    @Nullable Short getRRMPolicyMarginMinRation();

}

