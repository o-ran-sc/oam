package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import java.lang.String;
import org.eclipse.jdt.annotation.Nullable;
import org.opendaylight.yangtools.yang.binding.DataObject;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * grouping SupiRange {
 *   leaf start {
 *     type string;
 *   }
 *   leaf end {
 *     type string;
 *   }
 *   leaf pattern {
 *     type string;
 *   }
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/SupiRange</i>
 *
 */
public interface SupiRange
    extends
    DataObject
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("SupiRange");

    /**
     * @return <code>java.lang.String</code> <code>start</code>, or <code>null</code> if not present
     */
    @Nullable String getStart();
    
    /**
     * @return <code>java.lang.String</code> <code>end</code>, or <code>null</code> if not present
     */
    @Nullable String getEnd();
    
    /**
     * @return <code>java.lang.String</code> <code>pattern</code>, or <code>null</code> if not present
     */
    @Nullable String getPattern();

}

