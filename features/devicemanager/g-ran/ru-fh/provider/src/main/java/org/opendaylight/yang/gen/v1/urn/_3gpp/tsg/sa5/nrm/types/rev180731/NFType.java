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

public enum NFType implements Enumeration {
    NRF(0, "NRF"),
    
    UDM(1, "UDM"),
    
    AMF(2, "AMF"),
    
    SMF(3, "SMF"),
    
    AUSF(4, "AUSF"),
    
    NEF(5, "NEF"),
    
    PCF(6, "PCF"),
    
    SMSF(7, "SMSF"),
    
    NSSF(8, "NSSF"),
    
    UDR(9, "UDR"),
    
    LMF(10, "LMF"),
    
    GMLC(11, "GMLC"),
    
    _5GEIR(12, "5G_EIR"),
    
    SEPP(13, "SEPP"),
    
    UPF(14, "UPF"),
    
    N3IWF(15, "N3IWF"),
    
    AF(16, "AF"),
    
    UDSF(17, "UDSF"),
    
    BSF(18, "BSF"),
    
    CHF(19, "CHF")
    ;

    private static final Map<String, NFType> NAME_MAP;
    private static final Map<Integer, NFType> VALUE_MAP;

    static {
        final Builder<String, NFType> nb = ImmutableMap.builder();
        final Builder<Integer, NFType> vb = ImmutableMap.builder();
        for (NFType enumItem : NFType.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private NFType(int value, String name) {
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
     * @return corresponding NFType item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<NFType> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding NFType item, or null if no such item exists
     */
    public static NFType forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
