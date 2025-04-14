import streamlit as st

def params_tab(tab):
    with tab:
        st.subheader("Query Parameters")
        if 'params' not in st.session_state:
            st.session_state.params = [{"key": "", "value": ""}]

        for i, param in enumerate(st.session_state.params):
            cols = st.columns([3, 3, 1])
            key = cols[0].text_input("Key", param["key"], key=f"param_key_{i}")
            value = cols[1].text_input("Value", param["value"], key=f"param_value_{i}")
            if cols[2].button("❌", key=f"del_param_{i}"):
                st.session_state.params.pop(i)
                st.rerun()
            st.session_state.params[i] = {"key": key, "value": value}

        if st.button("+ Add Parameter"):
            st.session_state.params.append({"key": "", "value": ""})
            st.rerun()

        return st.session_state.params
