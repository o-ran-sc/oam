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

public enum TAvailabilityStatus implements Enumeration {
    /**
     * The resource is undergoing a test procedure. If the administrativestate is 
     * locked or shutting down then normal users are precluded from usingthe resource 
     * and the control status attribute has the value reserved for test.Tests that do 
     * not exclude additional users can be present in any operationalor administrative 
     * state but the reserved for test condition should not bepresent.
     *
     */
    INTEST(0, "IN TEST"),
    
    /**
     * The resource has an internal fault that prevents it from operating.The 
     * operational state is disabled.
     *
     */
    FAILED(1, "FAILED"),
    
    /**
     * The resource requires power to be applied and is not powered on.For example, a 
     * fuse or other protection device is known to have removedpower or a low voltage 
     * condition has been detected. The operational stateis disabled.
     *
     */
    POWEROFF(2, "POWER OFF"),
    
    /**
     * The resource requires a routine operation to be performed to placeit online and 
     * make it available for use. The operation may be manual orautomatic, or both. The
     * operational state is disabled.
     *
     */
    OFFLINE(3, "OFF LINE"),
    
    /**
     * The resource has been made inactive by an internal control processin accordance 
     * with a predetermined time schedule. Under normal conditionsthe control process 
     * can be expected to reactivate the resource at somescheduled time, and it is 
     * therefore considered to be optional. Theoperational state is enabled or 
     * disabled.
     *
     */
    OFFDUTY(4, "OFF DUTY"),
    
    /**
     * The resource cannot operate because some other resource on which itdepends is 
     * (i.e. a resource not represented by the same managed object)unavailable. For 
     * example, a device is not accessible because its controlleris powered off. The 
     * operational state is disabled.
     *
     */
    DEPENDENCY(5, "DEPENDENCY"),
    
    /**
     * The service available from the resource is degraded in some respect,such as in 
     * speed or operating capacity. Failure of a test or an unacceptableperformance 
     * measurement has established that some or all services are notfunctional or are 
     * degraded due to the presence of a defect. However, theresource remains available
     * for service, either because some services aresatisfactory or because degraded 
     * service is preferable to no service at all.Object specific attributes may be 
     * defined to represent further informationindicating, for example, which services 
     * are not functional and the nature ofthe degradation. The operational state is 
     * enabled.
     *
     */
    DEGRADED(6, "DEGRADED"),
    
    /**
     * The resource represented by the managed object is not present, or isincomplete. 
     * For example, a plug-in module is missing, a cable is disconnectedor a software 
     * module is not loaded. The operational state is disabled.
     *
     */
    NOTINSTALLED(7, "NOT INSTALLED"),
    
    /**
     * This indicates a log full condition.
     *
     */
    LOGFULL(8, "LOG FULL")
    ;

    private static final Map<String, TAvailabilityStatus> NAME_MAP;
    private static final Map<Integer, TAvailabilityStatus> VALUE_MAP;

    static {
        final Builder<String, TAvailabilityStatus> nb = ImmutableMap.builder();
        final Builder<Integer, TAvailabilityStatus> vb = ImmutableMap.builder();
        for (TAvailabilityStatus enumItem : TAvailabilityStatus.values()) {
            vb.put(enumItem.value, enumItem);
            nb.put(enumItem.name, enumItem);
        }

        NAME_MAP = nb.build();
        VALUE_MAP = vb.build();
    }

    private final String name;
    private final int value;

    private TAvailabilityStatus(int value, String name) {
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
     * @return corresponding TAvailabilityStatus item, if present
     * @throws NullPointerException if name is null
     */
    public static Optional<TAvailabilityStatus> forName(String name) {
        return Optional.ofNullable(NAME_MAP.get(Objects.requireNonNull(name)));
    }

    /**
     * Return the enumeration member whose {@link #getIntValue()} matches specified value.
     *
     * @param intValue integer value
     * @return corresponding TAvailabilityStatus item, or null if no such item exists
     */
    public static TAvailabilityStatus forValue(int intValue) {
        return VALUE_MAP.get(intValue);
    }
}
