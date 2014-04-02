<RelativeLayout xmlns:android="http://schemas.android.com/apk/res/android"
    xmlns:tools="http://schemas.android.com/tools"
    android:layout_width=<#if buildApi lt 8 >"fill_parent"<#else>"match_parent"</#if>
    android:layout_height=<#if buildApi lt 8 >"fill_parent"<#else>"match_parent"</#if> >

    <TextView
        android:layout_width="wrap_content"
        android:layout_height="wrap_content"
        android:layout_centerHorizontal="true"
        android:layout_centerVertical="true"
        android:padding="@dimen/padding_medium"
        android:text="@string/hello_world"
        tools:context=".${activityClass}" />

</RelativeLayout>
