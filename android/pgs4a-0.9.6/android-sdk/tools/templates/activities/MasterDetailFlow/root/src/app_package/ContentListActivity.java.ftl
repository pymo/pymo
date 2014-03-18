package ${packageName};

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.NavUtils;
import android.view.MenuItem;

public class ${CollectionName}Activity extends FragmentActivity
        implements ${CollectionName}Fragment.Callbacks {

    private boolean mTwoPane;

    @Override
    public void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_${collection_name});
        <#if parentActivityClass != "">
        getActionBar().setDisplayHomeAsUpEnabled(true);
        </#if>

        if (findViewById(R.id.${detail_name}_container) != null) {
            mTwoPane = true;
            ((${CollectionName}Fragment) getSupportFragmentManager()
                    .findFragmentById(R.id.${collection_name}))
                    .setActivateOnItemClick(true);
        }
    }
    <#if parentActivityClass != "">

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        switch (item.getItemId()) {
            case android.R.id.home:
                NavUtils.navigateUpFromSameTask(this);
                return true;
        }
        return super.onOptionsItemSelected(item);
    }
    </#if>

    @Override
    public void onItemSelected(String id) {
        if (mTwoPane) {
            Bundle arguments = new Bundle();
            arguments.putString(${DetailName}Fragment.ARG_ITEM_ID, id);
            ${DetailName}Fragment fragment = new ${DetailName}Fragment();
            fragment.setArguments(arguments);
            getSupportFragmentManager().beginTransaction()
                    .replace(R.id.${detail_name}_container, fragment)
                    .commit();

        } else {
            Intent detailIntent = new Intent(this, ${DetailName}Activity.class);
            detailIntent.putExtra(${DetailName}Fragment.ARG_ITEM_ID, id);
            startActivity(detailIntent);
        }
    }
}
