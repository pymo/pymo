package ${packageName};

import android.os.Bundle;
import android.app.Activity;
import android.view.Menu;
import android.view.MenuItem;
import android.support.v4.app.NavUtils;

public class ${activityClass} extends Activity {

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.${layoutName});
        <#if parentActivityClass != "">
        getActionBar().setDisplayHomeAsUpEnabled(true);
        </#if>
    }

    @Override
    public boolean onCreateOptionsMenu(Menu menu) {
        getMenuInflater().inflate(R.menu.${menuName}, menu);
        return true;
    }
    <#include "include_onOptionsItemSelected.java.ftl">
}
