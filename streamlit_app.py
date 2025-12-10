with col_fee:
    st.markdown("### 💰 料金明細（自動計算）")

    play_fee, loc_fee, option_fee, total = calc_total(
        inp_play_time, loc_choice, loc_extra, inp_options, option_other_fee, inp_extra_fee
    )

    fee_html = f"""
    <div style="
        background-color: #ffffff;
        padding: 18px;
        border-radius: 14px;
        border: 1px solid #e0e0e0;
        box-shadow: 0 3px 10px rgba(0,0,0,0.12);
        margin-bottom: 20px;
        font-size: 16px;
        line-height: 1.6;
    ">
        <div style="margin-bottom: 10px;">
            <strong>プレイ料金：</strong> {jpy(play_fee)}
        </div>

        <div style="margin-bottom: 10px;">
            <strong>場所料金：</strong> {jpy(loc_fee)}
            <span style="color:#666;">（{loc_choice}）</span>
        </div>

        <div style="margin-bottom: 10px;">
            <strong>オプション料金：</strong> {jpy(option_fee)}
        </div>
    """

    if inp_extra_fee:
        fee_html += f"""
        <div style="margin-bottom: 10px;">
            <strong>特別追加料金：</strong> {jpy(inp_extra_fee)}
        </div>
        """

    fee_html += f"""
        <hr style="margin: 14px 0; border-top: 1px solid #ddd;" />

        <div style="font-size: 20px; font-weight: bold; color:#e91e63; text-align:right;">
            合計：{jpy(total)}
        </div>
    </div>
    """

    st.markdown(fee_html, unsafe_allow_html=True)
