package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping aMFIdentifier {
 *   leaf AMF-Region-id {
 *     type t_aMF-Region-id;
 *   }
 *   leaf AMF-Set-id {
 *     type t_aMF-Set-id;
 *   }
 *   leaf AMF-Pointer {
 *     type t_aMF-Pointer;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/aMFIdentifier</i>
 *
 */
public interface AMFIdentifier
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("aMFIdentifier");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TAMFRegionId</code> <code>aMFRegionId</code>, or <code>null</code> if not present
     */
    @Nullable TAMFRegionId getAMFRegionId();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TAMFSetId</code> <code>aMFSetId</code>, or <code>null</code> if not present
     */
    @Nullable TAMFSetId getAMFSetId();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TAMFPointer</code> <code>aMFPointer</code>, or <code>null</code> if not present
     */
    @Nullable TAMFPointer getAMFPointer();

}

