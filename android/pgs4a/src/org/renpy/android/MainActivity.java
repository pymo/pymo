package org.renpy.android;

import android.app.TabActivity;
import android.content.Intent;
import android.content.pm.PackageManager;
import android.content.res.Resources;
import android.graphics.Color;
import android.Manifest;
import android.os.Bundle;
import android.support.v4.app.ActivityCompat;
import android.support.v4.content.ContextCompat;
import android.view.View;
import android.widget.TabHost;
import android.widget.TabWidget;
import android.widget.TextView;
import android.widget.TabHost.OnTabChangeListener;
import android.widget.Toast;
import android.util.DisplayMetrics;
import android.util.Log;


public class MainActivity extends TabActivity {
    private TabHost mTabHost;
    private TabWidget mTabWidget;
    private ResourceManager resourceManager;
    public static final int PERMISSION_ALL = 123;

    private void CreateLayout() {
        View current_view = resourceManager.inflateView("main");
        setContentView(current_view);

        mTabHost = this.getTabHost();
        mTabHost.setPadding(mTabHost.getPaddingLeft(),
            mTabHost.getPaddingTop(), mTabHost.getPaddingRight(),
            mTabHost.getPaddingBottom() - 5);

        Intent layout1intent = new Intent();
        layout1intent.setClass(this, FileChooser.class);
        TabHost.TabSpec layout1spec = mTabHost.newTabSpec("layout1");
        layout1spec.setIndicator(null,
            resourceManager.getDrawable("ic_menu_archive"));
        layout1spec.setContent(layout1intent);
        mTabHost.addTab(layout1spec);

        Intent layout2intent = new Intent();
        layout2intent.setClass(this, Config.class);
        TabHost.TabSpec layout2spec = mTabHost.newTabSpec("layout2");
        layout2spec.setIndicator(null,
            resourceManager.getDrawable("ic_menu_manage"));
        layout2spec.setContent(layout2intent);
        mTabHost.addTab(layout2spec);

        mTabWidget = mTabHost.getTabWidget();
        for (int i = 0; i < mTabWidget.getChildCount(); i++) {
            View view = mTabWidget.getChildAt(i);
            if (mTabHost.getCurrentTab() == i) {
                view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_d"));
            } else {
                view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_n"));
            }
            DisplayMetrics displaymetrics = new DisplayMetrics();
            getWindowManager().getDefaultDisplay().getMetrics(displaymetrics);
            if (displaymetrics.widthPixels > displaymetrics.heightPixels) {
                mTabWidget.getChildAt(i).getLayoutParams().height = displaymetrics.heightPixels / 10;
            } else {
                mTabWidget.getChildAt(i).getLayoutParams().height = displaymetrics.heightPixels / 18;
            }
            TextView tv = (TextView) mTabWidget.getChildAt(i).findViewById(
                android.R.id.title);
            tv.setTextColor(Color.rgb(255, 255, 255));
        }

        mTabHost.setOnTabChangedListener(new OnTabChangeListener() {
            @Override
            public void onTabChanged(String tabId) {
                for (int i = 0; i < mTabWidget.getChildCount(); i++) {
                    View view = mTabWidget.getChildAt(i);
                    if (mTabHost.getCurrentTab() == i) {
                        view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_d"));
                    } else {
                        view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_n"));
                    }
                }
            }
        });
    }

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);

        resourceManager = new ResourceManager(this);
        if (android.os.Build.VERSION.SDK_INT >= android.os.Build.VERSION_CODES.M) {
            // For Mashmallow and above, request for read/write SD card.
            // Check if the permission has been granted
            if (ContextCompat.checkSelfPermission(this, Manifest.permission.READ_EXTERNAL_STORAGE) !=
                PackageManager.PERMISSION_GRANTED ||
                ContextCompat.checkSelfPermission(this, Manifest.permission.WRITE_EXTERNAL_STORAGE) !=
                PackageManager.PERMISSION_GRANTED) {
                // Permission is missing and must be requested.
                ActivityCompat.requestPermissions(this,
                    new String[] {
                        Manifest.permission.READ_EXTERNAL_STORAGE, Manifest.permission.WRITE_EXTERNAL_STORAGE
                    }, PERMISSION_ALL);
            } else {
                CreateLayout();
            }
        } else {
            CreateLayout();
        }
    }

    @Override
    public void onRequestPermissionsResult(int requestCode, String[] permissions, int[] grantResults) {
        super.onRequestPermissionsResult(requestCode, permissions, grantResults);
        if (requestCode == PERMISSION_ALL) {
            boolean all_granted = (permissions.length > 0);
            for (int result: grantResults) {
                if (result != PackageManager.PERMISSION_GRANTED) all_granted = false;
            }
            if (all_granted) {
                CreateLayout();
            } else {
                // Permission Denied
                Toast.makeText(this, resourceManager.getString("parent_folder"),
                    Toast.LENGTH_LONG).show();
                finish();
            }
        }
    }
}
