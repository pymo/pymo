package ${packageName};

import android.content.Intent;
import android.os.Bundle;
import android.support.v4.app.FragmentActivity;
import android.support.v4.app.NavUtils;
import android.view.MenuItem;

public class ${DetailName}Activity extends FragmentActivity {

    @Override
    protected void onCreate(Bundle savedInstanceState) {
        super.onCreate(savedInstanceState);
        setContentView(R.layout.activity_${detail_name});

        getActionBar().setDisplayHomeAsUpEnabled(true);

        if (savedInstanceState == null) {
            Bundle arguments = new Bundle();
            arguments.putString(${DetailName}Fragment.ARG_ITEM_ID,
                    getIntent().getStringExtra(${DetailName}Fragment.ARG_ITEM_ID));
            ${DetailName}Fragment fragment = new ${DetailName}Fragment();
            fragment.setArguments(arguments);
            getSupportFragmentManager().beginTransaction()
                    .add(R.id.${detail_name}_container, fragment)
                    .commit();
        }
    }

    @Override
    public boolean onOptionsItemSelected(MenuItem item) {
        if (item.getItemId() == android.R.id.home) {
            NavUtils.navigateUpTo(this, new Intent(this, ${CollectionName}Activity.class));
            return true;
        }

        return super.onOptionsItemSelected(item);
    }
}
