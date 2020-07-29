package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.base.MoreObjects;
import com.google.common.collect.ImmutableList;
import java.io.Serializable;
import java.lang.Override;
import java.lang.String;
import java.util.List;
import java.util.Objects;
import java.util.regex.Pattern;
import org.opendaylight.yangtools.yang.binding.CodeHelpers;
import org.opendaylight.yangtools.yang.binding.TypeObject;

public class TTAC
 implements TypeObject, Serializable {
    private static final long serialVersionUID = -7663797870532797015L;
    public static final List<String> PATTERN_CONSTANTS = ImmutableList.of("^(?:[a-fA-F0-9]*)$");
    private static final Pattern patterns = Pattern.compile(PATTERN_CONSTANTS.get(0));
    private static final String regexes = "[a-fA-F0-9]*";
    private final String _string;


    private static void check_stringLength(final String value) {
        final int length = value.length();
        if (length == 4) {
            return;
        }
        CodeHelpers.throwInvalidLength("[[4..4]]", value);
    }
    public TTAC(String _string) {
        super();
        check_stringLength(_string);
        
        this._string = _string;
    }
    /**
     * Creates a copy from Source Object.
     *
     * @param source Source object
     */
    public TTAC(TTAC source) {
        this._string = source._string;
    }
    
    /**
     * Return a String representing the value of this union.
     *
     * @return String representation of this union's value.
     */
    public String stringValue() {
        if (_string != null) {
            return _string;
        }
    
        throw new IllegalStateException("No value assinged");
    }


    public String getString() {
        return _string;
    }


    @Override
    public int hashCode() {
        return CodeHelpers.wrapperHashCode(_string);
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
        TTAC other = (TTAC) obj;
        if (!Objects.equals(_string, other._string)) {
            return false;
        }
        return true;
    }

    @Override
    public String toString() {
        final MoreObjects.ToStringHelper helper = MoreObjects.toStringHelper(TTAC.class);
        CodeHelpers.appendValue(helper, "_string", _string);
        return helper.toString();
    }
}

