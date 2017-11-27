#define feature
default {
    state_entry() {
        #if !feature
        llOwnerSay("Feature Enabled!");
        #endif
    }
}
