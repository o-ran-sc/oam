package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import com.google.common.collect.ImmutableList;
import java.beans.ConstructorProperties;
import java.io.Serializable;
import java.lang.Override;
import java.lang.String;
import java.util.List;
import java.util.Objects;
import java.util.regex.Pattern;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class SupportedFeatures
 implements TypeObject, Serializable {
    private static final long serialVersionUID = 237085469237900179L;
    public static final List<String> PATTERN_CONSTANTS = ImmutableList.of("^(?:[A-Fa-f0-9]*)$");
    private static final Pattern patterns = Pattern.compile(PATTERN_CONSTANTS.get(0));
    private static final String regexes = "[A-Fa-f0-9]*";
    private final String _value;

    private static void check_valueLength(final String value) {
    }

    @ConstructorProperties("value")
    public SupportedFeatures(String _value) {
        if (_value != null) {
            check_valueLength(_value);
        }
    
        Objects.requireNonNull(_value, "Supplied value may not be null");
        CodeHelpers.checkPattern(_value, patterns, regexes);
    
        this._value = _value;
    }
    
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public SupportedFeatures(SupportedFeatures source) {
        this._value = source._value;
    }

    public static SupportedFeatures getDefaultInstance(String defaultValue) {
        return new SupportedFeatures(defaultValue);
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
        SupportedFeatures other = (SupportedFeatures) obj;
        if (!Objects.equals(_value, other._value)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(SupportedFeatures.class);
        CodeHelpers.appendValue(helper, "_value", _value);
        return helper.toString();
    }
}

