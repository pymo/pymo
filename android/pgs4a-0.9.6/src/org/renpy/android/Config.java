package org.renpy.android;

import java.io.BufferedReader;
import java.io.File;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.FileWriter;
import java.io.IOException;

import android.app.Activity;
import android.app.AlertDialog;
import android.content.DialogInterface;
import android.content.Intent;
import android.net.Uri;
import android.os.Bundle;
import android.view.View;
import android.widget.Button;
import android.widget.CheckBox;
import android.widget.CompoundButton;

public class Config extends Activity
{    
	private CheckBox original_ratio=null; 
	private CheckBox keypad_extend=null; 
	private CheckBox keypad_horizontal=null; 
	private Button about_button=null; 
	private int set_executed_time=0;
	private int set_original_ratio = 0;
	private int set_keypad_extend = 0;
	private int set_keypad_horizontal = 1;
	private String set_last_path;
	private String line_read;

    private ResourceManager resourceManager;
    @Override
    public void onCreate(Bundle savedInstanceState)
    {
        super.onCreate(savedInstanceState);
        resourceManager = new ResourceManager(this);
        View current_view=resourceManager.inflateView("config");
        setContentView(current_view);
        original_ratio=(CheckBox)(resourceManager.getViewById(current_view,"original_ratio")); 
        keypad_extend=(CheckBox)(resourceManager.getViewById(current_view,"keypad_extend")); 
        keypad_horizontal=(CheckBox)(resourceManager.getViewById(current_view,"keypad_horizontal")); 
        about_button=(Button)(resourceManager.getViewById(current_view,"about_button")); 
        ReadSetting(getFilesDir()+"/globalconfig.txt");
        
        original_ratio.setOnCheckedChangeListener(cbListener);
        keypad_extend.setOnCheckedChangeListener(cbListener); 
        keypad_horizontal.setOnCheckedChangeListener(cbListener);
        
         about_button.setOnClickListener(new View.OnClickListener() {
             public void onClick(View v) {
                 About();
             }
         });

    }
    
	public void About() {
		AlertDialog.Builder builder = new AlertDialog.Builder(this);
		builder.setTitle(resourceManager.getString("info_title"));
		builder.setMessage(resourceManager.getString("info"));
		builder.setPositiveButton(resourceManager.getString("button_ok"), null);
		builder.setNegativeButton(resourceManager.getString("button_visit_website"),
				new DialogInterface.OnClickListener() {
					public void onClick(DialogInterface dialog, int whichButton) {
						Uri uri = Uri.parse("http://pymo.github.io");
						Intent web = new Intent(Intent.ACTION_VIEW, uri);
						startActivity(web);
					}
				});

		builder.create().show();
	}
	
    @Override
    public void onPause() {
        super.onPause();
        WriteSetting(getFilesDir()+"/globalconfig.txt");
    }    
    @Override
    public void onResume() {
        super.onResume();
        ReadSetting(getFilesDir()+"/globalconfig.txt");
    }
    private CheckBox.OnCheckedChangeListener cbListener =
            new CheckBox.OnCheckedChangeListener(){
           
            public void onCheckedChanged(CompoundButton buttonView,boolean isChecked)
            {
        		if (original_ratio.isChecked()) set_original_ratio=1;
        		else set_original_ratio=0;
        		if (keypad_extend.isChecked()) set_keypad_extend=1;
        		else set_keypad_extend=0;
        		if (keypad_horizontal.isChecked()) set_keypad_horizontal=1;
        		else set_keypad_horizontal=0;
            }
        }; 
	public void WriteSetting(String globalconfigpath) {
		FileWriter fw;
		try {
			fw = new FileWriter(globalconfigpath);
			fw.write("last_path,"+set_last_path+"\r\n");
			fw.write("executed_time,"+set_executed_time+"\r\n");
			fw.write("original_ratio,"+set_original_ratio+"\r\n");
			fw.write("keypad_extend,"+set_keypad_extend+"\r\n");
			fw.write("keypad_horizontal,"+set_keypad_horizontal+"\r\n");
			fw.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	public void ReadSetting(String globalconfigpath) {
		File globalconfig = new File(globalconfigpath);
		if (globalconfig.exists()) {
			try {
				BufferedReader br = new BufferedReader(new FileReader(globalconfig));
				line_read=br.readLine();
				while (line_read != null){
					String[] sArray=line_read.split(",");
					if (sArray[0].equals("last_path")) set_last_path =sArray[1];
					else if (sArray[0].equals("executed_time")) set_executed_time = Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("original_ratio")) set_original_ratio=Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("keypad_extend")) set_keypad_extend=Integer.parseInt(sArray[1]);
					else if (sArray[0].equals("keypad_horizontal")) set_keypad_horizontal=Integer.parseInt(sArray[1]);
					line_read=br.readLine();
				} 
				br.close();			
			} catch (FileNotFoundException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			} catch (IOException e) {
				// TODO Auto-generated catch block
				e.printStackTrace();
			}
		}

		if (set_original_ratio==0) original_ratio.setChecked(false);
		else original_ratio.setChecked(true);
		if (set_keypad_extend==0) keypad_extend.setChecked(false);
		else keypad_extend.setChecked(true);
		if (set_keypad_horizontal==0) keypad_horizontal.setChecked(false);
		else keypad_horizontal.setChecked(true);
	}

}

