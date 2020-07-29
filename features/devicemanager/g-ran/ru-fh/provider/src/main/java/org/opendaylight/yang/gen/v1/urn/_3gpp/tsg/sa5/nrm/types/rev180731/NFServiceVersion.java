package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.lang.String;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.DateAndTime;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping NFServiceVersion {
 *   leaf apiVersionInUri {
 *     type string;
 *   }
 *   leaf apiFullVersion {
 *     type string;
 *   }
 *   leaf expiry {
 *     type yang:date-and-time;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/NFServiceVersion</i>
 *
 */
public interface NFServiceVersion
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("NFServiceVersion");

    /**
     * @return <code>java.lang.String</code> <code>apiVersionInUri</code>, or <code>null</code> if not present
     */
    @Nullable String getApiVersionInUri();
    
    /**
     * @return <code>java.lang.String</code> <code>apiFullVersion</code>, or <code>null</code> if not present
     */
    @Nullable String getApiFullVersion();
    
    /**
     * @return <code>org.opendaylight.yang.gen.v1.urn.ietf.params.xml.ns.yang.ietf.yang.types.rev130715.DateAndTime</code> <code>expiry</code>, or <code>null</code> if not present
     */
    @Nullable DateAndTime getExpiry();

}

