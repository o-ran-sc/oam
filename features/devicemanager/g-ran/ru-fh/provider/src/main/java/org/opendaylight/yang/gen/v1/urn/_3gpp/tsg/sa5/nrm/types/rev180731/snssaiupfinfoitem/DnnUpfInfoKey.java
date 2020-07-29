package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.snssaiupfinfoitem;
import com.google.common.base.MoreObjects;
import java.lang.Override;
import java.lang.String;
import java.util.Objects;
import org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731.TDnn;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.Identifier;

public class DnnUpfInfoKey
 implements Identifier<DnnUpfInfo> {
    private static final long serialVersionUID = -3246452801435528856L;
    private final TDnn _dnn;


    public DnnUpfInfoKey(TDnn _dnn) {
    
    
        this._dnn = _dnn;
    }
    
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public DnnUpfInfoKey(DnnUpfInfoKey source) {
        this._dnn = source._dnn;
    }


    public TDnn getDnn() {
        return _dnn;
    }


    @Override
    public int hashCode() {
        return CodeHelpers.wrapperHashCode(_dnn);
    }

    @Override
    public boolean equals(java.lang.Object obj) {
        if (this == obj) {
            return true;
        }
        if (obj == null) {
            return false;
        }
        if (getClass() != obj.getClass()) {
            return false;
        }
        DnnUpfInfoKey other = (DnnUpfInfoKey) obj;
        if (!Objects.equals(_dnn, other._dnn)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(DnnUpfInfoKey.class);
        CodeHelpers.appendValue(helper, "_dnn", _dnn);
        return helper.toString();
    }
}

