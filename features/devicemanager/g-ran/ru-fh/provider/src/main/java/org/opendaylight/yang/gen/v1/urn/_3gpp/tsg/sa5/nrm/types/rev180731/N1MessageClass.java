package org.opendaylight.yang.gen.v1.urn._3gpp.tsg.sa5.nrm.types.rev180731;
import com.google.common.collect.ImmutableMap;
import com.google.common.collect.ImmutableMap.Builder;
import java.lang.Integer;
import java.lang.Override;
import java.lang.String;
import java.util.Map;
import java.util.Objects;
import java.util.Optional;
import org.opendaylight.yangtools.yang.binding.Enumeration;

public enum N1MessageClass implements Enumeration {
    _5GMM(0, "5GMM"),
    
    SM(1, "SM"),
    
    LPP(2, "LPP"),
    
    SMS(3, "SMS")
    ;

    private static final Map<String, N1MessageClass> NAME_MAP;
    private static final Map<Integer, N1MessageClass> VALUE_MAP;

    static {
        final Builder<String, N1MessageClass> nb = ImmutableMap.builder();
        final Builder<Integer, N1MessageClass> vb = ImmutableMap.builder();
        for (N1MessageClass enumItem : N1MessageClass.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private N1MessageClass(int value, String name) {
        this.value = value;
        this.name = name;
    }

    @Override
    public String getName() {
        return name;
    }

    @Override
    public int getIntValue() {
        return value;
    }

    /**
     * Return the enumeration member whose {@link #getName()} matches specified value.
     *
     * @param name YANG assigned name
     * @return corresponding N1MessageClass item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<N1MessageClass> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding N1MessageClass item, or null if no such item exists
     */
    public static N1MessageClass forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
