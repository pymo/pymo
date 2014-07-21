// pymo_packDlg.cpp : implementation file
//

#include "stdafx.h"
#include "pymo_pack.h"
#include "pymo_packDlg.h"
#include  <vector> 
using   namespace   std; 
#ifdef _DEBUG
#define new DEBUG_NEW
#undef THIS_FILE
static char THIS_FILE[] = __FILE__;
#endif
#define BIF_USENEWUI 0x0050
/////////////////////////////////////////////////////////////////////////////
// CAboutDlg dialog used for App About

class CAboutDlg : public CDialog
{
public:
	CAboutDlg();
	
	// Dialog Data
	//{{AFX_DATA(CAboutDlg)
	enum { IDD = IDD_ABOUTBOX };
	//}}AFX_DATA
	
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CAboutDlg)
protected:
	virtual void DoDataExchange(CDataExchange* pDX);    // DDX/DDV support
	//}}AFX_VIRTUAL
	
	// Implementation
protected:
	//{{AFX_MSG(CAboutDlg)
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};

CAboutDlg::CAboutDlg() : CDialog(CAboutDlg::IDD)
{
	//{{AFX_DATA_INIT(CAboutDlg)
	//}}AFX_DATA_INIT
}

void CAboutDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CAboutDlg)
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CAboutDlg, CDialog)
//{{AFX_MSG_MAP(CAboutDlg)
// No message handlers
//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPymo_packDlg dialog

CPymo_packDlg::CPymo_packDlg(CWnd* pParent /*=NULL*/)
: CDialog(CPymo_packDlg::IDD, pParent)
{
	//{{AFX_DATA_INIT(CPymo_packDlg)
	m_strPath = _T("");
	m_sRtDataFilePath = _T("");
	//}}AFX_DATA_INIT
	// Note that LoadIcon does not require a subsequent DestroyIcon in Win32
	m_hIcon = AfxGetApp()->LoadIcon(IDR_MAINFRAME);
}

void CPymo_packDlg::DoDataExchange(CDataExchange* pDX)
{
	CDialog::DoDataExchange(pDX);
	//{{AFX_DATA_MAP(CPymo_packDlg)
	DDX_Text(pDX, IDC_EDIT1, m_strPath);
	DDX_Text(pDX, IDC_EDIT2, m_sRtDataFilePath);
	//}}AFX_DATA_MAP
}

BEGIN_MESSAGE_MAP(CPymo_packDlg, CDialog)
//{{AFX_MSG_MAP(CPymo_packDlg)
ON_WM_SYSCOMMAND()
ON_WM_PAINT()
ON_WM_QUERYDRAGICON()
ON_BN_CLICKED(IDC_BUTTON1, OnButton1)
	ON_BN_CLICKED(IDC_BUTTON2, OnButton2)
	//}}AFX_MSG_MAP
END_MESSAGE_MAP()

/////////////////////////////////////////////////////////////////////////////
// CPymo_packDlg message handlers

BOOL CPymo_packDlg::OnInitDialog()
{
	CDialog::OnInitDialog();
	
	// Add "About..." menu item to system menu.
	
	// IDM_ABOUTBOX must be in the system command range.
	ASSERT((IDM_ABOUTBOX & 0xFFF0) == IDM_ABOUTBOX);
	ASSERT(IDM_ABOUTBOX < 0xF000);
	
	CMenu* pSysMenu = GetSystemMenu(FALSE);
	if (pSysMenu != NULL)
	{
		CString strAboutMenu;
		strAboutMenu.LoadString(IDS_ABOUTBOX);
		if (!strAboutMenu.IsEmpty())
		{
			pSysMenu->AppendMenu(MF_SEPARATOR);
			pSysMenu->AppendMenu(MF_STRING, IDM_ABOUTBOX, strAboutMenu);
		}
	}
	
	// Set the icon for this dialog.  The framework does this automatically
	//  when the application's main window is not a dialog
	SetIcon(m_hIcon, TRUE);			// Set big icon
	SetIcon(m_hIcon, FALSE);		// Set small icon
	
	// TODO: Add extra initialization here
	
	return TRUE;  // return TRUE  unless you set the focus to a control
}

void CPymo_packDlg::OnSysCommand(UINT nID, LPARAM lParam)
{
	if ((nID & 0xFFF0) == IDM_ABOUTBOX)
	{
		CAboutDlg dlgAbout;
		dlgAbout.DoModal();
	}
	else
	{
		CDialog::OnSysCommand(nID, lParam);
	}
}

// If you add a minimize button to your dialog, you will need the code below
//  to draw the icon.  For MFC applications using the document/view model,
//  this is automatically done for you by the framework.

void CPymo_packDlg::OnPaint() 
{
	if (IsIconic())
	{
		CPaintDC dc(this); // device context for painting
		
		SendMessage(WM_ICONERASEBKGND, (WPARAM) dc.GetSafeHdc(), 0);
		
		// Center icon in client rectangle
		int cxIcon = GetSystemMetrics(SM_CXICON);
		int cyIcon = GetSystemMetrics(SM_CYICON);
		CRect rect;
		GetClientRect(&rect);
		int x = (rect.Width() - cxIcon + 1) / 2;
		int y = (rect.Height() - cyIcon + 1) / 2;
		
		// Draw the icon
		dc.DrawIcon(x, y, m_hIcon);
	}
	else
	{
		CDialog::OnPaint();
	}
}

// The system calls this to obtain the cursor to display while the user drags
//  the minimized window.
HCURSOR CPymo_packDlg::OnQueryDragIcon()
{
	return (HCURSOR) m_hIcon;
}

void CPymo_packDlg::OnButton1() 
{
	// TODO: Add your control notification handler code here
	UpdateData(TRUE);
	char szDir[MAX_PATH];
	BROWSEINFO bi;
	ITEMIDLIST *pidl;
	bi.hwndOwner = this->m_hWnd;
	bi.pidlRoot = NULL;
	bi.pszDisplayName = szDir;
	bi.lpszTitle = "Choose dir to be packed";
	bi.ulFlags = BIF_STATUSTEXT | BIF_USENEWUI | BIF_RETURNONLYFSDIRS;
	bi.lpfn = NULL;
	bi.lParam = 0;
	bi.iImage = 0;
	pidl = SHBrowseForFolder(&bi);
	if(pidl == NULL)  return;
	if(!SHGetPathFromIDList(pidl, szDir))   return;
	else  m_strPath = szDir;
	UpdateData(FALSE);    
}

void CPymo_packDlg::OnButton2() 
{
	// TODO: Add your control notification handler code here
	char szFilter[]="pymo pak files(*.pak)|*.pak";
	
	CFileDialog dlg(1,NULL,NULL,NULL,szFilter);
	
	if(dlg.DoModal()==IDOK)
	{
        m_sRtDataFilePath = dlg.GetPathName();
		if (m_sRtDataFilePath.Right(4)!=".pak"){
		    m_sRtDataFilePath+=".pak";
		}
	}
	UpdateData(FALSE);
}

void CPymo_packDlg::OnOK() 
{
	// TODO: Add extra validation here
	UpdateData(TRUE);
	char nullstring[]="\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0\0";
	char*   buf;
    CString m_cstrFileList="";
    CFileFind tempFind;
    CString strTmp;
	CFile file,pakfile;
	unsigned int filelength,fileoffset,contentoffset,i,filenamelength,filecount,realoffset;
    BOOL bFound;
    vector <int> offsetlist,lengthlist;
    vector <CString> filenamelist;
    fileoffset=0;
    bFound=tempFind.FindFile(m_strPath+"\\*.*");
    while(bFound)
    {
        bFound=tempFind.FindNextFile();
		if(tempFind.IsDots() || tempFind.IsDirectory())
			continue;
		else{
			strTmp=tempFind.GetFileName();
			filenamelist.push_back(strTmp);
			file.Open(m_strPath+"\\"+strTmp, CFile::modeRead);
			filelength=(unsigned int)file.GetLength();
			lengthlist.push_back(filelength);
			offsetlist.push_back(fileoffset);
			fileoffset+=filelength;
			file.Close();
		}
		
    }
    tempFind.Close();
	contentoffset=filenamelist.size()*(32+4*2)+4;
	filecount=filenamelist.size();
	pakfile.Open(m_sRtDataFilePath, CFile::modeCreate|CFile::modeWrite);
	pakfile.Write(&filecount, sizeof(unsigned int));
	for (i=0;i<filecount;i++){
		filenamelength=filenamelist[i].ReverseFind('.');
		if(filenamelength!=-1){
			strTmp=filenamelist[i];
			strTmp.MakeUpper();
			pakfile.Write(strTmp.GetBuffer(0), filenamelength);
			pakfile.Write(nullstring, 32-filenamelength);
			realoffset=offsetlist[i]+contentoffset;
			pakfile.Write(&(realoffset), sizeof(unsigned int));
			pakfile.Write(&(lengthlist[i]), sizeof(unsigned int));
		}
	}
	for (i=0;i<filecount;i++){
		file.Open(m_strPath+"\\"+filenamelist[i], CFile::modeRead);
		buf=new   char[lengthlist[i]];
		file.Read(buf,lengthlist[i]); 
		pakfile.Write(buf, lengthlist[i]);
		delete   (buf);
		file.Close();
	}
	pakfile.Close();
	strTmp.Format( "%d files are packed.",filecount); 
	MessageBox(strTmp,NULL);
	//CDialog::OnOK();
}
