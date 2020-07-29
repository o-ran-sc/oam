package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.top.rev180731;
import java.lang.String;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TDistinguishedName;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-top</b>
 * <pre>
 * grouping TopGrp {
 *   leaf objectClass {
 *     type string;
 *   }
 *   leaf id {
 *     type nrm-type:t_DistinguishedName;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-top/TopGrp</i>
 *
 */
public interface TopGrp
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("TopGrp");

    /**
     * @return <code>java.lang.String</code> <code>objectClass</code>, or <code>null</code> if not present
     */
    @Nullable String getObjectClass();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TDistinguishedName</code> <code>id</code>, or <code>null</code> if not present
     */
    @Nullable TDistinguishedName getId();

}

