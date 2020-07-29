package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami.AmfId;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami.PlmnId;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping Guami {
 *   container plmnId {
 *     uses pLMNId;
 *   }
 *   container amfId {
 *     uses aMFIdentifier;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/Guami</i>
 *
 */
public interface Guami
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("Guami");

    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami.PlmnId</code> <code>plmnId</code>, or <code>null</code> if not present
     */
    @Nullable PlmnId getPlmnId();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.guami.AmfId</code> <code>amfId</code>, or <code>null</code> if not present
     */
    @Nullable AmfId getAmfId();

}

