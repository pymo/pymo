// pymo_unpack.h : main header file for the PYMO_UNPACK application
//

#if !defined(AFX_PYMO_UNPACK_H__5F1BBDD0_E76B_4C68_AA9E_0CD3D9A0A601__INCLUDED_)
#define AFX_PYMO_UNPACK_H__5F1BBDD0_E76B_4C68_AA9E_0CD3D9A0A601__INCLUDED_

#if _MSC_VER > 1000
#pragma once
#endif // _MSC_VER > 1000

#ifndef __AFXWIN_H__
	#error include 'stdafx.h' before including this file for PCH
#endif

#include "resource.h"		// main symbols

/////////////////////////////////////////////////////////////////////////////
// CPymo_unpackApp:
// See pymo_unpack.cpp for the implementation of this class
//

class CPymo_unpackApp : public CWinApp
{
public:
	CPymo_unpackApp();

// Overrides
	// ClassWizard generated virtual function overrides
	//{{AFX_VIRTUAL(CPymo_unpackApp)
	public:
	virtual BOOL InitInstance();
	//}}AFX_VIRTUAL

// Implementation

	//{{AFX_MSG(CPymo_unpackApp)
		// NOTE - the ClassWizard will add and remove member functions here.
		//    DO NOT EDIT what you see in these blocks of generated code !
	//}}AFX_MSG
	DECLARE_MESSAGE_MAP()
};


/////////////////////////////////////////////////////////////////////////////

//{{AFX_INSERT_LOCATION}}
// Microsoft Visual C++ will insert additional declarations immediately before the previous line.

#endif // !defined(AFX_PYMO_UNPACK_H__5F1BBDD0_E76B_4C68_AA9E_0CD3D9A0A601__INCLUDED_)
