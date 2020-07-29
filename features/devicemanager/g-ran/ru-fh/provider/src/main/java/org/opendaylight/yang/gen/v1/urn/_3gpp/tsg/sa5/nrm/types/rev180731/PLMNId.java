package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 * A Public Land Mobile Network is uniquely identified by its PLMN identifier. 
 * PLMN-Id consists of Mobile Country Code (MCC) and Mobile Network Code (MNC).
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping pLMNId {
 *   leaf MCC {
 *     type t_mcc;
 *   }
 *   leaf MNC {
 *     type t_mnc;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/pLMNId</i>
 *
 */
public interface PLMNId
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("pLMNId");

    /**
     * Mobile Country Code (MCC), consisting of three decimal digits.The MCC identifies
     * uniquely the country of domicile of the mobile subscription.
     *
     *
     *
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TMcc</code> <code>mCC</code>, or <code>null</code> if not present
     */
    @Nullable TMcc getMCC();
    
    /**
     * Mobile Network Code (MNC), consisting of two or three decimal digits.The MNC 
     * identifies the home PLMN of the mobile subscription.
     *
     *
     *
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TMnc</code> <code>mNC</code>, or <code>null</code> if not present
     */
    @Nullable TMnc getMNC();

}

