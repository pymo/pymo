<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <application>
        <activity android:name=".${CollectionName}Activity"
            android:label="@string/title_${collection_name}">
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

        <activity android:name=".${DetailName}Activity"
            android:label="@string/title_${detail_name}">
            <meta-data android:name="android.support.PARENT_ACTIVITY"
                android:value=".${CollectionName}Activity" />
        </activity>
    </application>

</manifest>
