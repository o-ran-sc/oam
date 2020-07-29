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

public enum N2InformationClass implements Enumeration {
    SM(0, "SM"),
    
    NRPPa(1, "NRPPa"),
    
    PWS(2, "PWS"),
    
    PWSBCAL(3, "PWS-BCAL"),
    
    PWSRF(4, "PWS-RF")
    ;

    private static final Map<String, N2InformationClass> NAME_MAP;
    private static final Map<Integer, N2InformationClass> VALUE_MAP;

    static {
        final Builder<String, N2InformationClass> nb = ImmutableMap.builder();
        final Builder<Integer, N2InformationClass> vb = ImmutableMap.builder();
        for (N2InformationClass enumItem : N2InformationClass.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private N2InformationClass(int value, String name) {
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
     * @return corresponding N2InformationClass item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<N2InformationClass> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding N2InformationClass item, or null if no such item exists
     */
    public static N2InformationClass forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
