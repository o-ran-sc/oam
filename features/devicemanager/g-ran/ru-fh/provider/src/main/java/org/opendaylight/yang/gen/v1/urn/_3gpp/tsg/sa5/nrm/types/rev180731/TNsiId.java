package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import java.beans.ConstructorProperties;
import java.io.Serializable;
import java.lang.Override;
import java.lang.String;
import java.util.Objects;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TNsiId
 implements TypeObject, Serializable {
    private static final long serialVersionUID = 5629408106052088513L;
    private final String _value;


    @ConstructorProperties("value")
    public TNsiId(String _value) {
    
        Objects.requireNonNull(_value, "Supplied value may not be null");
    
        this._value = _value;
    }
    
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public TNsiId(TNsiId source) {
        this._value = source._value;
    }

    public static TNsiId getDefaultInstance(String defaultValue) {
        return new TNsiId(defaultValue);
    }

    public String getValue() {
        return _value;
    }


    @Override
    public int hashCode() {
        return CodeHelpers.wrapperHashCode(_value);
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
        TNsiId other = (TNsiId) obj;
        if (!Objects.equals(_value, other._value)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TNsiId.class);
        CodeHelpers.appendValue(helper, "_value", _value);
        return helper.toString();
    }
}

