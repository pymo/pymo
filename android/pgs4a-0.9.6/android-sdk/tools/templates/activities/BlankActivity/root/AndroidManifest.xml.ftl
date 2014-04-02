<manifest xmlns:android="http://schemas.android.com/apk/res/android" >

    <application>
        <activity android:name=".${activityClass}"
            android:label="@string/title_${activityToLayout(activityClass)}">
            <#if parentActivityClass != "">
            <meta-data android:name="android.support.PARENT_ACTIVITY"
                android:value="${parentActivityClass}" />
            <#else>
            <intent-filter>
                <action android:name="android.intent.action.MAIN" />
                <category android:name="android.intent.category.LAUNCHER" />
            </intent-filter>
            </#if>
        </activity>
    </application>

</manifest>
