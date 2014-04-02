package org.renpy.android;

import android.app.TabActivity;
import android.content.Intent;
import android.content.res.Resources;
import android.graphics.Color;
import android.os.Bundle;
import android.view.View;
import android.widget.TabHost;
import android.widget.TabWidget;
import android.widget.TextView;
import android.widget.TabHost.OnTabChangeListener;

public class MainActivity extends TabActivity
{
    private TabHost mTabHost;
    private TabWidget mTabWidget;
    private ResourceManager resourceManager;

    /** Called when the activity is first created. */
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        resourceManager = new ResourceManager(this);
        View current_view=resourceManager.inflateView("main");
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
        for (int i = 0; i < mTabWidget.getChildCount(); i++)
        {
            View view = mTabWidget.getChildAt(i);
            if (mTabHost.getCurrentTab() == i)
            {
                view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_d"));
            }
            else
            {
                view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_n"));
            }
            mTabWidget.getChildAt(i).getLayoutParams().height = 70;
            TextView tv = (TextView) mTabWidget.getChildAt(i).findViewById(
                    android.R.id.title);
            tv.setTextColor(Color.rgb(255,255,255));
        }

        mTabHost.setOnTabChangedListener(new OnTabChangeListener()
        {
            @Override
            public void onTabChanged(String tabId)
            {
                for (int i = 0; i < mTabWidget.getChildCount(); i++)
                {
                    View view = mTabWidget.getChildAt(i);
                    if (mTabHost.getCurrentTab() == i)
                    {
                        view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_d"));
                    }
                    else
                    {
                        view.setBackgroundDrawable(resourceManager.getDrawable("home_btn_bg_n"));
                    }
                }
            }
        });
    }
}
