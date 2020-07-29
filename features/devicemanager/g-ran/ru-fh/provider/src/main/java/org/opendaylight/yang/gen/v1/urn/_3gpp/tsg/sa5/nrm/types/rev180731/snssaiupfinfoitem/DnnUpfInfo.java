package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.snssaiupfinfoitem;
import java.lang.Override;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.$YangModuleInfoImpl;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.DnnUpfInfoItem;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.SnssaiUpfInfoItem;
import org.opendaylight.yangtools.yang.binding.Augmentable;
import org.opendaylight.yangtools.yang.binding.ChildOf;
import org.opendaylight.yangtools.yang.binding.Identifiable;
import org.opendaylight.yangtools.yang.common.QName;

/**
 *
 * <p>
 * This class represents the following YANG schema fragment defined in module <b>_3gpp-common-yang-types</b>
 * <pre>
 * list dnnUpfInfo {
 *   key dnn;
 *   uses DnnUpfInfoItem;
 * }
 * </pre>The schema path to identify an instance is
 * <i>_3gpp-common-yang-types/SnssaiUpfInfoItem/dnnUpfInfo</i>
 *
 * <p>To create instances of this class use {@link DnnUpfInfoBuilder}.
 * @see DnnUpfInfoBuilder
 * @see DnnUpfInfoKey
 *
 */
public interface DnnUpfInfo
    extends
    ChildOf<SnssaiUpfInfoItem>,
    Augmentable<DnnUpfInfo>,
    DnnUpfInfoItem,
    Identifiable<DnnUpfInfoKey>
{



    public static final QName QNAME = $YangModuleInfoImpl.qnameOf("dnnUpfInfo");

    @Override
    DnnUpfInfoKey key();

}

