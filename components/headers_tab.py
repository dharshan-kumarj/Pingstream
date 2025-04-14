import streamlit as st

def headers_tab(tab):
    with tab:
        st.subheader("Headers")
        if 'headers' not in st.session_state:
            st.session_state.headers = [{"key": "", "value": ""}]

        for i, header in enumerate(st.session_state.headers):
            cols = st.columns([3, 3, 1])
            key = cols[0].text_input("Key", header["key"], key=f"header_key_{i}")
            value = cols[1].text_input("Value", header["value"], key=f"header_value_{i}")
            if cols[2].button("❌", key=f"del_header_{i}"):
                st.session_state.headers.pop(i)
                st.rerun()
            st.session_state.headers[i] = {"key": key, "value": value}

        if st.button("+ Add Header"):
            st.session_state.headers.append({"key": "", "value": ""})
            st.rerun()

        return st.session_state.headers
